# This is a Flask-powered server
from flask import Flask, render_template, make_response, json, request, Response
from werkzeug.datastructures import Headers
import os
from Scripts.term_highlighter import TermHighlighter

MODES = ["Biology", "Geography", "Physics"]
app = Flask(__name__)
try:
    term_highlighter = TermHighlighter(MODES)
except:
    pass
@app.route('/')
def mainPage():
    return render_template("mainPage.html", availableModes=MODES)
@app.route('/highlightWithMode')
def highlightText():
    term_highlighter.use_mode(request.args["mode"])
    response_json = json.JSONEncoder().encode({"highlightedText":term_highlighter.highlight_text(request.args["text"])})
    return Response(response_json, headers=Headers([('Content-Type', 'application/json')]))
