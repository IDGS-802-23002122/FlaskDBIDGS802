from wtforms import Form
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, EmailField, RadioField
from wtforms import validators
from wtforms.validators import DataRequired, NumberRange


class UserForm2(Form): 
    id = IntegerField('Id', [
        validators.DataRequired(message="El campo es requerido"),
        validators.NumberRange(min=100, max=1000, message="Ingrese un valor valido")
    ])

    nombre = StringField('Nombre', [
        validators.DataRequired(message="El campo es requerido"),
        validators.length(min=3, max=10, message="Ingrese un nombre valido")
    ])

    apaterno = StringField('Apaterno', [
        validators.DataRequired(message="El campo es requerido")
    ])

    amaterno = StringField('Amaterno', [
        validators.DataRequired(message="El campo es requerido")
    ])

    email = EmailField('Correo', [
        validators.DataRequired(message="El campo es requerido"),
        validators.Email(message="Correo no valido")
    ])
    
    contrasenia = PasswordField('Contrasenia')

class CinepolisForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    compradores = IntegerField('Compradores', validators=[DataRequired(), NumberRange(min=1)])
    boletos = IntegerField('Boletos', validators=[DataRequired(), NumberRange(min=1)])
    tarjeta = RadioField('Tarjeta', choices=[('si', 'Sí'), ('no', 'No')], default='no')