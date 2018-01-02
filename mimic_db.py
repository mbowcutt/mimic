from mimic import app, markovify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from werkzeug.utils import secure_filename

import os

## Upload restrictions
ALLOWED_EXTENSIONS = set(['txt'])
app.config['UPLOAD_FOLDER'] = '/tmp'
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 # 16 Mb upload limit

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mimic.db'
db = SQLAlchemy(app)
migrate=Migrate(app,db)

class Persona(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    model = db.Column(db.Text, nullable=False)
    source = db.Column(db.Text, nullable=False)

class Alias(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    persona = db.relationship("Persona", backref="aliases", lazy=True)
    persona_name = db.Column(db.String(80), db.ForeignKey("persona.name"), nullable=False)

db.create_all()

def createOrUpdatePersona(person, name, model, source):
    if not person:
        person = Persona(name=name, model=model.to_json(), source = source)
        registerAlias(person, name)
        db.session.add(person)
    else:
        model_old = markovify.Text.from_json(person.model)
        model_new = markovify.combine([model_old, model])
        person.model = model_new.to_json()
    db.session.commit()
    return

def readPersona(name): 
    return Persona.query.filter_by(name=name).first()

def registerAlias(persona, name):
    alias=Alias(name=name.lower(), persona=persona, persona_name=persona.name)
    persona.aliases.append(alias)
    db.session.commit()

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS