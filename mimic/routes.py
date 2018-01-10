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
            alias = Alias.query.filter_by(name=name.lower()).first()
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
    if action=="persona":
        if request.method == 'POST':
            if(request.form['action']=="delete"):
                deletePersona(person)
                return redirect(url_for("index"))
            else:
                upload(request, name, person)

        return redirect(url_for("profile", name=name, action="manage"))

    elif action=="alias":
        if request.method=="POST":
            alias=request.form['alias']
            if alias=="":
                flash("No given alias")
                return redirect(url_for("profile", name=name, action="manage"))
            if not person:
                flash("Persona does not exist")
                return redirect(url_for("profile", name=name, action="manage"))
            else:
                if(request.form['action']=="delete"):
                    unregisterAlias(person, alias)
                else:
                    registerAlias(person, alias)
                return redirect(url_for("profile", name=name, action="manage"))
        else:
            alias=request.args.get('delete')
            if alias=="":
                flash("No given alias")
                return redirect(url_for("profile", name=name, action="manage"))
            if not person:
                flash("Persona does not exist")
                return redirect(url_for("profile", name=name, action="manage"))
            else:
                unregisterAlias(person, alias)
                return redirect(url_for("profile", name=name, action="manage"))

    elif action=="manage":
        if not person:
            return render_template("enrollment.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(), name=name, exist=False)
        else:
            aliases=person.aliases
            return render_template("enrollment.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(), name=name, exist=True, aliases=aliases, aliasform=PersonaAliasForm())
    
    else:
        if not person:
            return redirect(url_for("profile", name=name, action="manage"))
        return render_template("utter.html", search=PersonaSearchForm(), upload=PersonaEnrollmentForm(),
                                name=name, engine = markovify.Text.from_json(person.model))

@app.route("/")
def index():
    return render_template("index.html", search=PersonaSearchForm())