from flask import flash, request, redirect, url_for, render_template

from mimic.forms import *
from mimic.data import *
from mimic.uploads import *

@app.route("/explore", methods=['GET', 'POST'])
def explore():
    if request.method == "POST":
        name = request.form['name']
        if not name:
            return redirect("/explore")
        else:
            alias = readAlias(name)
            if not alias:
                return redirect(url_for("profile", name=name, action="utter"))
            else:
                return redirect(url_for("profile", name=alias.persona.name, action="utter"))
    return render_template("explore.html", search=PersonaSearchForm(),
                            personas=db.session.query(Persona.name).all())

@app.route("/develop")
def develop():
    return render_template("developers.html", search=PersonaSearchForm())

@app.route("/<name>/<action>", methods=['GET', 'POST'])
def profile(name, action):
    person = readPersona(name)
    if action=="init":
        if not person:
            createPersona(name)
        return redirect(url_for("manage", name=name))

    elif action=="delete":
        deletePersona(person)
        return redirect(url_for("manage", name=name))

    elif action=="markovify":
        if not person:
            return redirect(url_for("manage", name=name))
        return render_template("markovify.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(),
                                name=name, engine = markovify.Text.from_json(person.model))

    elif action=="alias":
        if not person or request.method=="GET":
            return redirect(url_for("manage", name=name))

        alias=request.form['alias']
        if alias=="":
            flash("No given alias")
            return redirect(url_for("manage", name=name))

        if(request.form['action']=="delete"):
            unregisterAlias(person, alias)
        elif(request.form['action']=="add"):
            registerAlias(person, alias)
        return redirect(url_for("manage", name=name))

    elif action=="source":
        if not person or request.method=="GET":
            return redirect(url_for("manage", name=name))

        if (request.form['action']=="delete"):
            removeSource(person, request.form['title']);
            ## TODO: Retrain persona

        elif(request.form['action']=="add"):
            title = request.form['title'];
            description = request.form['description']
            uri = request.form['uri']
            addSource(person, title, description, uri);
            ## TODO: Retrain Persona
    
    return redirect(url_for("manage", name=name))
        
    
@app.route("/<name>")
def manage(name):
    person = readPersona(name)
    if not person:
        return render_template("enrollment.html", search=PersonaSearchForm(), name=name, exist=False)
    else:
        return render_template("enrollment.html", search=PersonaSearchForm(), name=name, exist=True, person=person, aliasform=PersonaAliasForm(), sourceform=SourceControlForm())

@app.route("/")
def index():
    return render_template("index.html", search=PersonaSearchForm())