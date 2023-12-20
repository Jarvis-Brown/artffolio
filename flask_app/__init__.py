from flask import Flask
import os

app = Flask(__name__)

# Calculate the relative path to the "static" folder
app_root = os.path.dirname(os.path.abspath(__file__))
static_folder = os.path.join(app_root, 'static')

# Set the "static" folder configuration
app.static_folder = static_folder


app.secret_key = "projects"