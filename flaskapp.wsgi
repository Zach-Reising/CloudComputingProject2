import sys
import os

# Path to your project
project_home = '/home/ubuntu/CloudComputingProject2'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Path to the virtual environment site-packages
venv_path = '/home/ubuntu/CloudComputingProject2/venv/lib/python3.11/site-packages'
if venv_path not in sys.path:
    sys.path.insert(0, venv_path)

# Set environment variable for Flask
os.environ['FLASK_APP'] = 'flaskapp'

# Import Flask app
from flaskapp import app as application
