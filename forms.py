# forms.py
from flask_wtf import FlaskForm
from wtforms import StringField, DateField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
import re

def password_complexity(form, field): # Password complexity
    pattern = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$") # Check the password to this regex pattern
    if not pattern.match(field.data):
        raise ValidationError(
            "The Password has to be at least 8 digets long and needs" # Error if complexity not met
            "one uppercase, one lowercase and a number!"
        )

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), password_complexity]) # Use the password_complexity for checking
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')]) # Same password given twice
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class CertificateForm(FlaskForm):
    common_name = StringField('Common Name', validators=[DataRequired()])
    creation_date = DateField('Creation Date', validators=[DataRequired()])
    valid_to_date = DateField('Valid To Date', validators=[DataRequired()])
    comments = TextAreaField('Comments')
    zip_password = PasswordField('Zip Password')
    pfx_password = PasswordField('PFX Password')
    submit = SubmitField('Add Certificate') # Submitbutton for adding new certificate
    submitedit = SubmitField('Edit Certificate') # Submitbutton for editing a certifiacte