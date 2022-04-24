
apt-get update
apt-get install g++
apt-get install unixodbc-dev
apt-get install mssql-tools unixodbc-dev -y
gunicorn -w 4 -k uvicorn.workers.UvicornWorker App.main:app