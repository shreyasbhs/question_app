from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import login


question_belongs_to_topic = db.Table( 'question_belongs_to_topic',
    db.Column('id',db.Integer,primary_key = True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id')),
    db.Column('topic_id',db.Integer,db.ForeignKey('topic.id'))
   )

company_asks_question = db.Table( 'company_asks_question',
    db.Column('id',db.Integer,primary_key = True),
    db.Column('question_id',db.Integer,db.ForeignKey('question.id')),
    db.Column('company_id',db.Integer, db.ForeignKey('company.id'))
    )

student_solves_question = db.Table('student_solves_question',
    db.Column('id',db.Integer,primary_key = True),
    db.Column('question_id',db.Integer, db.ForeignKey('question.id')),
    db.Column('user_id',db.Integer, db.ForeignKey('user.id'))
    )

class User(UserMixin,db.Model):
    id = db.Column(db.Integer,primary_key = True)
    firstname = db.Column(db.String(30),index = True)
    lastname  = db.Column(db.String(30),index = True)
    username = db.Column(db.String(30),index = True,unique = True)
    email = db.Column(db.String(120),index = True,unique = True)
    password = db.Column(db.String(120))
    is_attempting = db.Column(db.Boolean,index = True)
    profile = db.relationship('Profile',backref = db.backref('profile'))
    solves = db.relationship('Question',secondary= student_solves_question,
            backref=db.backref('student'))

    def set_password(self,password):
        self.password = generate_password_hash(password)
    def check_password(self,password):
        return check_password_hash(self.password,password)
    def __rep__(self):
        return f'User {self.firstname}'
    

class Profile(db.Model):
    id = db.Column(db.Integer,db.ForeignKey('user.id'),primary_key=True)
    photo = db.Column(db.String(200),index=True)
    no_questions_solves = db.Column(db.Integer,index=True)
    no_questions_attempted =db.Column(db.Integer,index=True)
    success_rate = db.Column(db.Integer,index = True)
    rank = db.Column(db.Integer,index = True) 
class Admin(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    username = db.Column(db.String(50),index = True,unique = True)
    password = db.Column(db.String(50),index = True)
    question = db.relationship('Question',backref = db.backref('question'));

class Question(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(30),index = True,unique = True)
    content = db.Column(db.String(500),index = True)
    inputfile = db.Column(db.String(300),index = True)
    outputfile = db.Column(db.String(300),index = True)
    difficulty = db.Column(db.String(20),index = True)
    admin_id = db.Column(db.Integer,db.ForeignKey('admin.id'))
    belongs_to_topic = db.relationship('Topic',secondary= question_belongs_to_topic,
                      backref=db.backref('questions'))
    asked_by_company = db.relationship('Company',secondary= company_asks_question,
                      backref=db.backref('questions'))
class Topic(db.Model):
    id = db.Column(db.Integer,primary_key = True)
    name = db.Column(db.String(100),index= True,unique = True)
    popularity = db.Column(db.Integer)
    no_questions = db.Column(db.Integer)
    
    
class Company(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),index= True,unique = True)
    rating = db.Column(db.Integer)
    no_questions = db.Column(db.Integer)
    
    

    


@login.user_loader
def load_user(id):
    return User.query.get(int(id))