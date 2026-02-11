import sys
import os
import site

# Project path
project_home = '/home/ubuntu/CloudComputingProject2'
if project_home not in sys.path:
    sys.path.insert(0, project_home)

# Virtualenv site-packages
venv_site = '/home/ubuntu/CloudComputingProject2/venv/lib/python3.12/site-packages'
site.addsitedir(venv_site)

# Set environment (optional)
os.environ['FLASK_ENV'] = 'production'

# Import Flask app
from flaskapp import app as application
