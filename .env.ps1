# Activate the virtual environment
sas-venv\Scripts\Activate

# Set Flask environment variables
$env:FLASK_APP = "webserver\server.py"
$env:FLASK_ENV = "development"
