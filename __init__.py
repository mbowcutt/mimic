import os
from flask import Flask, flash, jsonify, request, redirect, url_for, send_from_directory, render_template, Blueprint
from werkzeug.utils import secure_filename
import markovify
import logging

# Initialize app
app = Flask(__name__)
app.secret_key=os.urandom(24)
logging.basicConfig(filename='app.log',level=logging.INFO)

from mimic.mimic_db import *
from mimic.forms import *

mimic = Blueprint('mimic', __name__,
                    template_folder="templates", static_folder="static")

@app.route("/")
@mimic.route("/")
def index():
    return render_template("index.html", search=PersonaSearchForm())

@app.route("/<name>", methods=['GET', 'POST'])
@mimic.route("/<name>", methods=['GET', 'POST'])
def persona(name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No 'file' file in form")
            return redirect(request.url)

        file = request.files['file']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(url_for("persona", name=name))

        #saveDocument(file)
        model = markovize(file)
        createOrUpdatePersona(name, model.to_json(), 'manual upload')

    person = readPersona(name)
    if not person:
        return render_template("enrollment.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(), name=name)
    return render_template("persona.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(),
                             person=person, engine = markovify.Text.from_json(person.model))

@app.route("/explore", methods=['GET', 'POST'])
@mimic.route("/explore", methods=['GET', 'POST'])
def explore():
    if request.method == "POST":
        name = request.form['name']
        if not name:
            return redirect("/explore")
        else:
            return redirect(url_for("persona", name=name))
    return render_template("explore.html", search=PersonaSearchForm(),
                            personas=db.session.query(Persona.name).all())

@app.route("/develop")
@mimic.route("/develop")
def develop():
    return render_template("developers.html", search=PersonaSearchForm())

def markovize(file):
        text=file.stream.read()
        model = markovify.Text(text.decode("utf-8"))
        return model

def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app.run()
