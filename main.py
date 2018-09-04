# This is a Flask-powered server
from flask import Flask, render_template
import os
app = Flask(__name__)

@app.route('/')
def mainPage():
    return render_template("mainPage.html", availableModes=["Biology", "Geography", "Wiki"])
