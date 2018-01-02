from mimic import app
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import Form, StringField
from wtforms.validators import DataRequired
from flask_uploads import UploadSet, TEXT

class PersonaSearchForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])

class PersonaEnrollmentForm(FlaskForm):
    file = FileField("Source Document", validators=[FileRequired()])

