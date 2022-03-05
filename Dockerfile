FROM python:3.8-slim-buster

# Create directories
RUN mkdir -p /app
RUN mkdir -p /log

# Set working directory
WORKDIR /app

# Install dependencies
COPY pip_packages.txt pip_packages.txt
RUN pip3 install -r pip_packages.txt

# Copy program over
COPY . /app

# Expose ports
EXPOSE 5000/tcp
EXPOSE 9100/tcp

# Run
ENTRYPOINT [ "python3" ]
CMD ["app.py"]
