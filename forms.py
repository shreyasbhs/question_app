from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from wtforms import widgets,SelectMultipleField
from wtforms import (StringField,PasswordField,BooleanField,SubmitField,
                     TextField,SelectField,HiddenField)
from wtforms.validators import ValidationError,DataRequired,Length,Email,EqualTo
from models import User,Admin,Question

class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()
class SignupForm(FlaskForm):
    firstname = StringField('firstname',validators= [DataRequired(),Length(min = 2,max = 25)])
    lastname = StringField('lastname',validators = [DataRequired(),Length(min = 2,max = 25)])
    email = StringField('email',validators = [DataRequired(),Email()])
    username = StringField('username',validators = [DataRequired(),Length(min = 2,max = 30)])
    password = PasswordField('password',validators = [DataRequired()])
    confirm = PasswordField('confirm',validators = [DataRequired(),EqualTo('password','passwords must match')])
    submit = SubmitField('sign up')
    def validate_username(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError('This username already exits.Choose some other username')
    
    def validate_email(self,email):
        user = User.query.filter_by(email = email.data).first()
        if user is not None:
            raise ValidationError('Account associated with this email already exits')
        
        


class LoginForm(FlaskForm):
    username = StringField('username',validators = [DataRequired(),Length(min = 2,max = 30)])
    password = PasswordField('password',validators = [DataRequired()])
    submit = SubmitField('sign in')


class AdminForm(FlaskForm):
    username = StringField('username',validators = [DataRequired(),Length(min = 2,max = 30)])
    password = PasswordField('password',validators = [DataRequired()])
    submit = SubmitField('sign in')
    

class CreateQuestion(FlaskForm):
    title = StringField('title',validators = [DataRequired(),Length(max = 30)])
    content = TextField('content')
    testcode = TextField('testcode',validators = [DataRequired()])
    inputfile = FileField('inputfile')
    output = HiddenField('output')
    submit= SubmitField('Add/update')
    company = MultiCheckboxField('company',choices = [('Amazon','Amazon'),('Oracle','Oracle'),('Adobe','Adobe'),('JP Morgan','JP Morgan'),
                                               ('Goldman Sacks','Goldman Sacks')])
    topic  = MultiCheckboxField('topic',choices = [('array','array'),('string','string'),('matrix','matrix'),
                                                    ('dp','dp'),('greedy','greedy'),('brut force','brut force')])
    
    def validate_title(self,title):
        q = Question.query.filter_by(title=title.data).first()
        if q is not None:
            raise ValidationError('This title already exists.Choose some other title')

        
    