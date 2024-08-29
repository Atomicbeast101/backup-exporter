# Prometheus Backup Exporter

Custom Prometheus exporter in Python for monitoring backup status in my homelab (personal datacenter). It runs as a Docker container in Kubernetes environment and it uses API endpoints to receive calls from backup scripts, update the backup status in SQLite database and report status by exposing the Prometheus metrics endpoint.

This repo contains a Docker CI/CD pipeline file to automatically build this container image in my self-hosted DevOps system.

## API Endpoint(s)

* [Update Backup Status for Service](api-docs/update-backup-status-for-service.md) : `POST /api/status/<service>`

## Prometheus Metrics Example

The `service` name that gets called in `POST` API call will show as `name` field below.

```
# HELP backup_status_timestamp Timestamp of last backup.
# TYPE backup_status_timestamp gauge
backup_status_timestamp{name="mongodb"} 1.724911203028333e+012
backup_status_timestamp{name="mariadb"} 1.724911203503168e+012
backup_status_timestamp{name="media"} 1.724911261490754e+012
backup_status_timestamp{name="house-db"} 1.724911432529975e+012
backup_status_timestamp{name="postgresql"} 1.724911440365695e+012
backup_status_timestamp{name="router"} 1.724918402932199e+012
```

