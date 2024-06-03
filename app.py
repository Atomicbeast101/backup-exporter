# Imports
import prometheus_client
import logging.handlers
import threading
import datetime
import logging
import sqlite3
import flask
import time
import os
import re

# Environment Variables
API_HOST = '0.0.0.0'
API_PORT = 5000
PROM_HOST = '0.0.0.0'
PROM_PORT = 9100
if os.getenv('API_HOST'):
    API_HOST = os.getenv('API_HOST')
if os.getenv('API_PORT'):
    API_PORT = int(os.getenv('API_PORT'))
if os.getenv('PROM_HOST'):
    PROM_HOST = os.getenv('PROM_HOST')
if os.getenv('PROM_PORT'):
    PROM_PORT = int(os.getenv('PROM_PORT'))

# Logging
logger = logging.getLogger("backup-exporter")
logger.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(message)s")
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
file_handler = logging.handlers.RotatingFileHandler(
    '/log/app.log',
    maxBytes=1*1000000, # 1MB
    backupCount=5
)
file_handler.setFormatter(formatter)
logger.addHandler(console_handler)
logger.addHandler(file_handler)
service_name_pattern = r'^[a-z\-]*$'

# Database
db = sqlite3.connect('data.db', check_same_thread=False)

# Attributes
metrics = {
    'backup_status_timestamp': prometheus_client.Gauge('backup_status_timestamp', 'Timestamp of last backup.', ['name'])
}
app = flask.Flask(__name__)

# Functions
def prepare_db():
    cur = db.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS backup_status (name, ts)')
    cur.close()

def to_timestamp(dt):
    return time.mktime(dt.timetuple()) * 1000 + dt.microsecond / 1000

def update_metrics():
    while True:
        metrics['backup_status_timestamp'].clear()
        cur = db.cursor()
        cur.execute('SELECT name, ts FROM backup_status')
        for row in cur.fetchall():
            metrics['backup_status_timestamp'].labels(name=row[0]).set(to_timestamp(datetime.datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S.%f')))
        cur.close()
        time.sleep(5)

@app.route('/api/status/<service>', methods=['POST'])
def status(service):
    service = service.lower()
    if re.match(service_name_pattern, service):
        # Update data
        ts = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

        # Update data in database
        cur = db.cursor()
        cur.execute("SELECT EXISTS(SELECT 1 FROM backup_status WHERE name = '%s')" % service)
        if cur.fetchone()[0] == 1:
            cur.execute("UPDATE backup_status SET ts='%s' WHERE name = '%s'" % (ts, service))
        else:
            cur.execute("INSERT INTO backup_status VALUES ('%s', '%s')" % (service, ts))
        db.commit()
        cur.close()
        
        return flask.jsonify({'success':True}), 200
    return flask.jsonify({'success': False, 'reason': 'Name must be all letters and/or - symbol only!'}), 400

# Main
def main():
    logger.info('Starting application...')
    logger.info('Preparing database...')
    prepare_db()
    logger.info('Database prepared!')

    # Start Prometheus exporter
    logger.info('Starting Prometheus exporter...')
    threading.Thread(target=update_metrics).start()
    prometheus_client.start_http_server(PROM_PORT, PROM_HOST)
    logger.info('Prometheus exporter started!')

    # Start flask
    logger.info('Started API endpoint!')
    app.run(host=API_HOST, port=API_PORT)

main()
