from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, FloatField, FileField, PasswordField, HiddenField
from wtforms.validators import InputRequired, Email, NumberRange
from flask_wtf.file import FileField, FileRequired, FileAllowed

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    status = SelectField('Fullname', validators=[InputRequired()], choices=["pending", "published"])
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png'], "Only images allowed!")
    ])
    user_id = HiddenField('User Id', validators=[InputRequired()])

class UserForm(FlaskForm):
    fullname = StringField('Name', validators=[InputRequired()])
    email = StringField('Email', validators=[InputRequired(), Email()])
    password = PasswordField('Password', validators=[InputRequired()])
    role = SelectField('Role', validators=[InputRequired()], choices=["Admin", "Regular"])