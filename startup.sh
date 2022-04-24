
apt-get update
apt-get install g++
apt-get install unixodbc-dev
apt-get install mssql-tools unixodbc-dev -y
apt-get install unixodbc unixodbc-dev freetds-dev freetds-bin tdsodbc
gunicorn -w 4 -k uvicorn.workers.UvicornWorker App.main:app