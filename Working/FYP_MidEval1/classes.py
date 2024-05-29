from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, EmailField, IntegerField
from wtforms.validators import InputRequired, Email, Length
from random import randint


class SignUpForm(FlaskForm):
    email = EmailField('Email', validators=[InputRequired(), Email()] , render_kw={"autocomplete": "EMAIL"})
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6, max=20)] , render_kw={"autocomplete": "current-password"})
    signup_as = SelectField('Sign up as', choices=[('Transporter', 'Transporter'), ('Industrialist', 'Industrialist'), ('Customer', 'Customer'), ('TruckDriver', 'TruckDriver')])

class TransporterSignUpForm(FlaskForm):
    transporter_name = StringField('Name', validators=[InputRequired(), Length(min=4, max=20)] , render_kw={"autocomplete": "username"})
    contact_number = StringField('ContactNumber', validators=[InputRequired(), Length(min=13, max=13)] , render_kw={"autocomplete": "contactnumber"})
    # email = EmailField('Email', validators=[InputRequired(), Email()] , render_kw={"autocomplete": "email"})
    address = StringField('Address', validators=[InputRequired(), Length(min=4, max=200)] , render_kw={"autocomplete": "address"})


class CustomerSignUpForm(FlaskForm):
    customer_name = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)] , render_kw={"autocomplete": "username"})
    contact_number = StringField('ContactNumber', validators=[InputRequired(), Length(min=13, max=13)] , render_kw={"autocomplete": "contactnumber"})
    # email = EmailField('Email', validators=[InputRequired(), Email()] , render_kw={"autocomplete": "email"})
    address = StringField('Address', validators=[InputRequired(), Length(min=4, max=200)] , render_kw={"autocomplete": "address"})


class IndustrialistSignUpForm(FlaskForm):
    industrialist_name = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)] , render_kw={"autocomplete": "username"})
    contact_number = StringField('ContactNumber', validators=[InputRequired(), Length(min=13, max=13)] , render_kw={"autocomplete": "contactnumber"})
    # email = EmailField('Email', validators=[InputRequired(), Email()] , render_kw={"autocomplete": "email"})
    address = StringField('Address', validators=[InputRequired(), Length(min=4, max=200)] , render_kw={"autocomplete": "address"})


class DriverSignUpForm(FlaskForm):
    driver_name = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)] , render_kw={"autocomplete": "username"})
    contact_number = StringField('ContactNumber', validators=[InputRequired(), Length(min=13, max=13)] , render_kw={"autocomplete": "contactnumber"})
    license_number = StringField('License' , validators = [InputRequired()] , render_kw={"autocomplete" : "license"})


def random_number_generator(n = 6):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)