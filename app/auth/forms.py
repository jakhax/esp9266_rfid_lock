from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,BooleanField,PasswordField
from wtforms.validators import Required,DataRequired,Length

class LoginForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(1, 32)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')