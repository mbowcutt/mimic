import os
from flask import Flask, flash, jsonify, request, redirect, url_for, send_from_directory, render_template, Blueprint
from flask_sqlalchemy import SQLAlchemy
from forms import PersonaSearchForm
from werkzeug.utils import secure_filename
import markovify
import logging

## Upload restrictions
UPLOAD_FOLDER='/tmp'
ALLOWED_EXTENSIONS = set(['txt'])

# Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mimic.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 # 16 Mb upload limit
logging.basicConfig(filename='app.log',level=logging.INFO)
db = SQLAlchemy(app)

# Persona class
class Persona(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    model = db.Column(db.Text, nullable=False)

db.create_all()

mimic = Blueprint('mimic', __name__,
                    template_folder="templates", static_folder="static")

@app.route("/")
@mimic.route("/")
def index():
    return render_template("layout.html")

@app.route("/<name>", methods=['GET', 'POST'])
@mimic.route("/<name>", methods=['GET', 'POST'])
def persona(name):
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No 'file' file in form")
            return redirect(request.url)
        if 'name' not in request.form:
            flash("No name field in form")
            return redirect(request.url)

        file = request.files['file']
        name = request.form['name']

        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if name == '':
            flash('No given name')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            model = markovize(filename)
            createOrUpdatePersona(name, model)
        return url_for(request.url)

    persona = Persona.query.filter_by(name=name).first()
    sentence = readPersona(name).make_sentence()
    return render_template("persona.html", persona=persona, sentence=sentence)

@app.route("/explore", methods=['GET', 'POST'])
@mimic.route("/explore", methods=['GET', 'POST'])
def explore():
    search = PersonaSearchForm(request.form)
    if request.method == 'POST':
        return url_for("/persona" + search.data['name'])
    return render_template("explore.html", form=search, personas=db.session.query(Persona.name).all())

def markovize(filename):
    with open(app.config['UPLOAD_FOLDER'] + "/" + filename) as f:
        text=f.read()
        return markovify.Text(text)

def createOrUpdatePersona(name, model):
    if not Persona.query.filter_by(name=name).first():
        person = Persona(name=name, model=model.to_json())
        db.session.add(person)
        db.session.commit()
        return
    else:
        person = Persona.query.filter_by(name=name).first()
        model_old = person.model
        model_new = markovify.combine(model_old, model)
        person.model = model_new.to_json()
        db.session.commit()
    return

def readPersona(name):
    person = Persona.query.filter_by(name=name).first()
    model = markovify.Text.from_json(person.model)
    return model


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app

if __name__ == "__main__":
    app.run()
