@echo off
call sas-venv\Scripts\activate
set FLASK_APP=webserver\server.py
set FLASK_ENV=development
