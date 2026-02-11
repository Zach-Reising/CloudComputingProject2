import sys
import os

sys.path.insert(0, "/home/ubuntu/CloudComputingProject2")

activate_this = '/home/ubuntu/CloudComputingProject2/venv/bin/activate_this.py'
with open(activate_this) as file:
    exec(file_.read), dict(__file__=activate_this)

from flaskapp import app as application
