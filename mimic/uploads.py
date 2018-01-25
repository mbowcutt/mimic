from flask import Flask, request, redirect, url_for, flash
from werkzeug.utils import secure_filename

from mimic.data import *

ALLOWED_EXTENSIONS = set(['txt'])

def upload(request, name, person):
    if 'file' not in request.files:
        flash("No 'file' file in form")
        return

    file = request.files['file']

    if file.filename == '':
        flash('No selected file')
        return

    model = markovize(file)
    if(request.form['action']=="create"):
        createPersona(name, model, 'manual upload')
    elif(request.form['action']=="update"):
        updatePersona(person, model)
    return