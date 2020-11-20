from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(30),index = True)
    lastname  = db.Column(db.String(30),index = True)
    username = db.Column(db.String(30),index = True,unique = True)
    email = db.Column(db.String(120),index = True,unique = True)
    password = db.Column(db.String(120))
   
    

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def __rep__(self):
        return f'User {self.firstname}'

class Admin(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),index = True,unique = True)
    password = db.Column(db.String(50),index = True)
    question = db.relationship('Question',backref = db.backref('question'));

class Question(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(30),index = True,unique = True)
    content = db.Column(db.String(3000),index = True)
    inputfile = db.Column(db.String(300),index = True)
    outputfile = db.Column(db.String(300),index = True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    
class Topic(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),index= True,unique = True)
    popularity = db.Column(db.Integer)
    no_questions = db.Column(db.Integer)
class Question_belongs_to_Topic(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id = db.Column(db.Integer,db.ForeignKey('question.id'))
    topic_id = db.Column(db.Integer,db.ForeignKey('topic.id'))
    
class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),index= True,unique = True)
    rating = db.Column(db.Integer)
    no_questions = db.Column(db.Integer)
    
    
class Company_asks_Question(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question = db.Column(db.Integer,db.ForeignKey('question.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    
class student_solves_question(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@login.user_loader
def load_user(id):
    return User.query.get(int(id))