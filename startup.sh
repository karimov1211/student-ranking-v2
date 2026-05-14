#!/bin/bash
# Install ODBC Driver for SQL Server
curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list
apt-get update
ACCEPT_EULA=Y apt-get install -y msodbcsql18 unixodbc-dev

# Start the application
gunicorn app:app -w 4 -k uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
