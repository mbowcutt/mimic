from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField
from wtforms.validators import DataRequired

class PersonaSearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class PersonaAliasForm(FlaskForm):
    alias = StringField('Alias', validators=[DataRequired()])

class PersonaEnrollmentForm(FlaskForm):
    file = FileField("Source Document", validators=[FileRequired()])

