import os
from flask import Flask, flash, jsonify, request, redirect, url_for, send_from_directory, render_template, Blueprint, session, g
from werkzeug.utils import secure_filename
import markovify
import logging

# Initialize app
app = Flask(__name__)
app.secret_key=os.urandom(24)
logging.basicConfig(filename='app.log',level=logging.INFO)

from mimic.data import *
from mimic.forms import *

mimic = Blueprint('mimic', __name__, template_folder="templates", static_folder="static")

@app.route("/")
@mimic.route("/")
def index():
    return render_template("index.html", search=PersonaSearchForm())

@app.route("/<name>/<action>", methods=['GET', 'POST'])
@mimic.route("/<name>/<action>", methods=['GET', 'POST'])
def persona(name, action):
    person = readPersona(name)
    if action=="persona":
        if request.method == 'POST':
            if(request.form['action']=="delete"):
                deletePersona(person)
                return redirect(url_for("index"))
            else:
                if 'file' not in request.files:
                    flash("No 'file' file in form")
                    return redirect(url_for("persona", name=name, action="manage"))

                file = request.files['file']

                # if user does not select file, browser also
                # submit a empty part without filename
                if file.filename == '':
                    flash('No selected file')
                    return redirect(url_for("persona", name=name, action="manage"))

                model = markovize(file)
                if(request.form['action']=="create"):
                    createPersona(name, model, 'manual upload')
                elif(request.form['action']=="update"):
                    updatePersona(person, model)

        return redirect(url_for("persona", name=name, action="manage"))

    elif action=="alias":
        if request.method=="POST":
            alias=request.form['alias']
            if alias=="":
                flash("No given alias")
                return redirect(url_for("persona", name=name, action="manage"))
            if not person:
                flash("Persona does not exist")
                return redirect(url_for("persona", name=name, action="manage"))
            else:
                if(request.form['action']=="delete"):
                    unregisterAlias(person, alias)
                else:
                    registerAlias(person, alias)
                return redirect(url_for("persona", name=name, action="manage"))
        else:
            alias=request.args.get('delete')
            if alias=="":
                flash("No given alias")
                return redirect(url_for("persona", name=name, action="manage"))
            if not person:
                flash("Persona does not exist")
                return redirect(url_for("persona", name=name, action="manage"))
            else:
                unregisterAlias(person, alias)
                return redirect(url_for("persona", name=name, action="manage"))

    elif action=="manage":
        if not person:
            return render_template("enrollment.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(), name=name, exist=False)
        else:
            aliases=person.aliases
            return render_template("enrollment.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(), name=name, exist=True, aliases=aliases, aliasform=PersonaAliasForm())
    
    else:
        if not person:
            return redirect(url_for("persona", name=name, action="manage"))
        return render_template("utter.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(),
                                name=name, engine = markovify.Text.from_json(person.model))

@app.route("/explore", methods=['GET', 'POST'])
@mimic.route("/explore", methods=['GET', 'POST'])
def explore():
    if request.method == "POST":
        name = request.form['name']
        if not name:
            return redirect("/explore")
        else:
            alias = Alias.query.filter_by(name=name.lower()).first()
            if not alias:
                return redirect(url_for("persona", name=name, action="utter"))
            else:
                return redirect(url_for("persona", name=alias.persona.name, action="utter"))
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
