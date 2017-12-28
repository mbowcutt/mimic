import os
import shelve
from flask import Flask, flash, jsonify, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

import markovify

import logging
logging.basicConfig(filename='app.log',level=logging.INFO)

UPLOAD_FOLDER='/tmp'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 # 16 Mb upload limit

@app.route("/")
def index():
    return render_template("layout.html")

@app.route("/personas")
def personas():
    db = shelve.open('personas.db')
    names = list(db.keys())
    db.close()
    return render_template("personas.html", names=names)

@app.route("/upload", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash("No 'file' file in form")
            return redirect(request.url)
        if 'name' not in request.form:
            flash("No name field in form")
            return redirect(request.url)
        if 'func' not in request.form:
            flash("No func field in form")

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
            setPersona(name, model)
    return render_template("upload.html")

@app.route("/utterance", methods=['GET','POST'])
def utterance():
    if request.method=='POST':
        if 'name' not in request.form:
            flash("No name field in form")
            return redirect("/personas")
        name = request.form['name']

        if name == '':
            flash('No persona selected')
            return redirect("/personas")
        sentence = getPersona(name).make_sentence()
    else:
        sentence = "/GET"
    return sentence

def markovize(filename):
    with open(app.config['UPLOAD_FOLDER'] + "/" + filename) as f:
        text=f.read()
        return markovify.Text(text)

def setPersona(name, model):
    db = shelve.open('personas.db')
    if (name in db):
        db[name] = markovify.combine([getPersona(name), model]).to_json()
    else:
        db[name] = model.to_json()
    db.close()

def getPersona(name):
    db = shelve.open('personas.db')
    model = markovify.Text.from_json(db[name])
    db.close()
    return model

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def create_app():
    app = Flask(__name__)
    return app

if __name__ == "__main__":
    app.run()
