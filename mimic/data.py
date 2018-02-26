from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from mimic import app
from mimic.engines import *

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mimic.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ALLOWED_EXTENSIONS = set(['txt'])
db = SQLAlchemy(app)
migrate=Migrate(app,db)

### OBJECTS

class Persona(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    model = db.Column(db.Text)

class Alias(db.Model):
    name = db.Column(db.String(80), primary_key=True)
    persona = db.relationship("Persona", backref="aliases", lazy=True)
    persona_name = db.Column(db.String(80), db.ForeignKey("persona.name"), nullable=False)

class Source(db.Model):
    title = db.Column(db.String(200), primary_key=True)
    description = db.Column(db.Text)
    uri = db.Column(db.Text, nullable = False)
    persona = db.relationship("Persona", backref="sources", lazy=True)
    persona_name = db.Column(db.String(80), db.ForeignKey("persona.name"), nullable=False)

db.create_all()

### PERSONA CRUD

def createPersona(name):
    person = Persona(name=name, model=None)
    registerAlias(person, name)
    db.session.add(person)
    db.session.commit()
    return

def readPersona(name): 
    return Persona.query.filter_by(name=name).first()

def deletePersona(persona):
    for alias in persona.aliases:
        db.session.delete(alias)
    for source in persona.sources:
        db.session.delete(source)
    db.session.delete(persona)
    db.session.commit()

### ALIAS CRUD

def registerAlias(persona, name):
    if(Alias.query.filter_by(name=name.lower()).first()):
        return
    else:
        alias=Alias(name=name.lower(), persona=persona, persona_name=persona.name)
        persona.aliases.append(alias)
        db.session.commit()

def unregisterAlias(persona, name):
    alias=readAlias(name)
    if alias.name == alias.persona.name.lower():
        return
    else:
        db.session.delete(alias)
        db.session.commit()

def readAlias(name):
    return Alias.query.filter_by(name=name.lower()).first()

### source CRUD

def addSource(persona, title, description, uri):
    source = Source(title=title, description=description, uri=uri, persona=persona, persona_name=persona.name)
    persona.sources.append(source)
    persona.model = markovize(persona);
    db.session.commit()

def removeSource(persona, title):
    source = Source.query.filter_by(title=title).first()
    db.session.delete(source);
    persona.model = markovize(persona);
    db.session.commit()
