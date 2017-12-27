import os
import shelve
from flask import Flask, flash, request, redirect, url_for, send_from_directory, render_template
from werkzeug.utils import secure_filename

db = shelve.open('personas.db')

# Markov chain text generator
import markovify

UPLOAD_FOLDER='/tmp'
ALLOWED_EXTENSIONS = set(['txt'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024 # 16 Mb upload limit

@app.route("/", methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            model = markovize(filename)
            

    return render_template('index.html')

@app.route("/utterance/{id}")
def utter(id):
    model = markovify.from_json(getPersona(id))
    return model.make_sentence()

def markovize(filename):
    with open(app.config['UPLOAD_FOLDER'] + "/" + filename) as f:
        text=f.read()
        return markovify.Text(text)

def setPersona(id, model):
    db[id] = model.to_json()

def getPersona(id):
    return markovify.Text.from_json(db[id])

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run()