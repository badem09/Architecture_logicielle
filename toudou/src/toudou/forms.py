import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, HiddenField, DateField, SelectField
from wtforms.validators import InputRequired

class FormModifier(FlaskForm):
    id = HiddenField("id", name="id")
    task = StringField(label='Intitulé : ', name="task", validators=[InputRequired()])
    status = SelectField(label='Status : ', name="status", choices=["Complétée", "Incomplète"])
    due = DateField(label="Date : ",name="due")

class FormAjouter(FlaskForm):
    task = StringField(label='Intitulé : ', name="task", validators=[InputRequired()])
    status = SelectField(label='Status : ', name="status", choices=["Complétée", "Incomplète"],
                         validators=[InputRequired()], default="Incomplète")
    due = DateField(label="Date : ", name="due", default=datetime.date.today())
