# This is a Flask-powered server
from flask import Flask, render_template, request, jsonify
from werkzeug.datastructures import Headers
import os
from Scripts.term_highlighter import TermHighlighter

app = Flask(__name__, )
MODES = ["Biology", "Geography", "Physics", "Wiki"]
try:
    term_highlighter = TermHighlighter(MODES)
except:
    term_highlighter = None

@app.route('/')
def mainPage():
    if term_highlighter is None:
        return render_template("mainPage.html", availableModes=MODES, status="Error loading resources", statusColor = "red")
    else:
        return render_template("mainPage.html", availableModes=MODES, status="Resources loaded successfully", statusColor = "rgb(94, 228, 11)")
@app.route('/highlightWithMode')
def highlightText():
    if term_highlighter is not None:
        term_highlighter.use_mode(request.args["mode"])
        response= {
            "highlightedText":term_highlighter.highlight_text(request.args["text"])
        }
        return jsonify(response)
    else:
        pass
