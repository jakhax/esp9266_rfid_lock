from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField
from wtforms.validators import Required,DataRequired,Length,Email

class CreateUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('submit')

class EditUserForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('submit')