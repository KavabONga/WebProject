# This is a Flask-powered server
from flask import Flask, render_template
import os
print(os.path.abspath('./Page'))
app = Flask(__name__)
Flask
@app.route('/')
def mainPage():
    return render_template("mainPage.html") # TODO: check if the flask app actually works
