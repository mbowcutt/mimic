from wtforms import Form, StringField, SelectField

class PersonaSearchForm(Form):
    search = StringField('')