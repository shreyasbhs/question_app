import os
from app import app
from werkzeug.datastructures import CombinedMultiDict
from flask import Flask,render_template,url_for,redirect,request,flash,session
from forms import (SignupForm,LoginForm,CreateQuestion,AdminForm)
from flask_login import current_user,login_user,logout_user
from models import (User,Question,Admin,Topic,
                    Company
                     )
from firebase import storage
from app import db
import random
from compiler import compile_it


basedir = 'C:\\Users\\user\\Desktop\\web\\flask\\practise\\practise2\\question_app\\'
@app.route('/',methods = ['GET', 'POST'])
@app.route('/<name>',methods = ['GET','POST'])
def home(name=""):
    questions = Question.query.all()
    companies = Company.query.all()
    topics = Topic.query.all()
    if request.method == 'POST':
        company = request.form['company']
        topic =request.form['topic']
        topic = Topic.query.filter_by(name = topic).first()
        company = Company.query.filter_by(name = company).first()
        questions_f = questions
        if company is not None:
            question_f = company.questions
            ctg = company.name
        else:
            question_f = questions
            ctg = ""
        if topic is not None:
            question_f = [question for question in question_f if question in topic.questions]
            ttg = topic.name
        else:
            question_f = [question for question in question_f]
            ttg = ""
        # inter = cq.intersection(tq)
        # question_f = list(inter)
        print(*question_f)
        return render_template('home.htm',name = name,questions = question_f,
                           companies = companies,topics = topics,ctg = ctg,ttg = ttg)
    return render_template('home.htm',name = name,questions = questions,
                           companies = companies,topics = topics,ctg = "",ttg = "")
    




@app.route('/signup',methods = ['GET','POST'])
def signup():
        
        form = SignupForm()
        if form.validate_on_submit():
            u = form
            user = User(firstname = u.firstname.data,lastname = u.lastname.data,
                    username = u.username.data,email = u.email.data, password = u.password.data,
                    is_attempting = False)
            user.set_password(u.password.data)
            db.session.add(user)
            db.session.commit()
            flash("You have registered sucessfully!!!","success")
            return redirect(url_for('login'))
        return render_template('signup.htm',form = form)



@app.route('/login',methods = ['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid User name or Password. Try again","error")
            return redirect(url_for('login'))
        login_user(user,remember = True)
        return redirect(url_for('home'))
    return render_template('login.htm',form = form)       


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/admin_login',methods = ['GET','POST'])
def admin_login ():
    form = AdminForm()
    if form.validate_on_submit():
        admin = Admin.query.filter_by(username = form.username.data).first()
        if admin is None or not admin.password==form.password.data:
            flash("Invalid User name or Password","error")
            return redirect(url_for('admin_login'))
        return redirect(url_for('admin',name = form.username.data))
    return render_template('admin_login.htm',form = form)

@app.route('/admin/<name>')
def admin(name):
    a = Admin.query.filter_by(username = name).first()
    questions = a.question
    return render_template('admin.htm',name = name,questions = questions)



@app.route('/<name>/new_problem',methods = ['GET','POST'])
def new_problem(name):
    form = CreateQuestion()
    if form.validate_on_submit():
        q = form
        ofile = q.title.data+'_o.txt'
        ifile = q.title.data+'_i.txt'
        #gerate inputfile
        q.inputfile.data.save('./'+ifile)
        
        storage.child('io/input/'+ifile).put('./'+ifile)
        os.remove(ifile)
        # f.close()
        #generate output file
        
        file = open('./'+ofile,'w')
        file.close()
        with open('./'+ofile,'w') as of:
            for line in q.output.data:
                line = line.rstrip('\n')
                of.write(line)
            of.close()
        storage.child('io/output/'+ofile).put('./'+ofile)
        
        # os.remove(ofile)  
            
        difficulty = q.difficulty.data
        que = Question(title  = q.title.data,content = q.content.data,
                      outputfile = ofile,inputfile = ifile,difficulty = difficulty)
       
        for topic in request.form.getlist('topic'):
            t = Topic.query.filter_by(name = topic).first()
            t.questions.append(que)
        for company in request.form.getlist('company'):
            c  = Company.query.filter_by(name = company).first()
            c.questions.append(que)
        
        db.session.add(que)
        db.session.commit()
        a = Admin.query.filter_by(username = name).first()
        a.question.append(que)
        db.session.commit()
        return redirect(url_for('admin',name = name))
    return render_template('new_problem.htm',name = name,form = form)

@app.route('/<name>/update_problem/<int:id>',methods = ['GET','POST'])
def update_problem(name,id):
    form = CreateQuestion()
    if request.method == 'GET':
     
        question = Question.query.filter_by(id = id).first()
        form.title.data = question.title
        form.content.data = question.content
        db.session.delete(question)
        db.session.commit()
    if form.validate_on_submit():
       
        q = form
        ofile = q.title.data+'_o.txt'
        ifile = q.title.data+'_i.txt'
        #gerate inputfile
        q.inputfile.data.save('./'+ifile)
        
        storage.child('io/input/'+ifile).put('./'+ifile)
        os.remove(ifile)
        # f.close()
        #generate output file
        
        file = open('./'+ofile,'w')
        file.close()
        with open('./'+ofile,'w') as of:
            for line in q.output.data:
                line = line.rstrip('\n')
                of.write(line)
            of.close()
        storage.child('io/output/'+ofile).put('./'+ofile)
        
        os.remove(ofile)  
            

            
            
            
        que = Question(title  = q.title.data,content = q.content.data,
                      outputfile = ofile,inputfile = ifile)
       
        for topic in request.form.getlist('topic'):
            t = Topic.query.filter_by(name = topic).first()
            t.questions.append(que)
        for company in request.form.getlist('company'):
            c  = Company.query.filter_by(name = company).first()
            c.questions.append(que)
        db.session.add(que)
        db.session.commit()
        a = Admin.query.filter_by(username = name).first()
        a.question.append(que)
        db.session.commit()
        flash(que.title+"has been updated")
        return redirect(url_for('admin',name = name))
    return render_template('update_problem.htm',name = name,id = id,form = form)
    

@app.route('/problems/<int:id>',methods = ['POST','GET'])
def problem(id):
        question = Question.query.filter_by(id = id).first()
        companies = []
        topics = []
        for c in Company.query.all():
            if question in c.questions:
                companies.append(c)
        for t in Topic.query.all():
            if question in t.questions:
                topics.append(t)
        fi = question.inputfile
        fo =question.outputfile
      
       
        
        customoutput = storage.child('io/output/'+fo).get_url(fo)
        custominput =   storage.child('io/input/'+fi).get_url(fi)
      
        if request.method == 'POST':
            if request.form['solved']=="true":
               flash("Well Done!!","success")
               code = request.form["code"]
               question  = Question.query.filter_by(id = id).first()
               if question not in current_user.solves:
                 current_user.solves.append(question)
               return render_template('problem.htm',result = "",code = code,
                                   inp = "",question = question,id = question.id,
                                   companies = companies,topics = topics,
                                   customoutput = customoutput,custominput = custominput);

                
        else:
            
            return render_template('problem.htm',result = "",code = "",
                                   inp = "",question = question,id = question.id,
                                   companies = companies,topics = topics,
                                   customoutput = customoutput,custominput = custominput);




@app.route('/<name>/mock_interview/',methods = ['GET','POST'])
def mock_interview(name):
    
    if(request.method=="POST"):
        #update codes
        #update time
       
        return redirect(url_for('home'))
    
    questions = Question.query.all()
    n = len(questions)
    q1 = questions[random.randint(0,n-1)]
    q2 = questions[random.randint(0,n-1)]
    q3 = questions[random.randint(0,n-1)]
    qs = [q1,q2,q3]
    inputs = []
    outputs = []
    for q in qs:
        fi = q.inputfile
        fo =q.outputfile
      
        storage.child('io/output/'+fo).download(fo)
        storage.child('io/input/'+fi).download(fi)
        custominput = open('./'+fi,'r').read()
        customoutput = open('./'+fo,'r').read()
        os.remove(fi)
        os.remove(fo)
        inputs.append(custominput)
        outputs.append(customoutput)
        print(custominput)
    else:
        # u = User.query.filter_by(username= name).first()
        # check = u.is_attempting
        # if not check:
        #     u.is_attempting = True
        #     db.session.commit()
        #     return render_template('mock_interview.htm',name = name,q1 = q1,q2 = q2,q3 = q3,inputs = inputs,outputs = outputs)
        # else:
        #     return render_template('not_allowed.htm')
        # return render_template('not_allowed.htm')
        return render_template('mock_interview.htm',name = name,q1 = q1,q2 = q2,q3 = q3,inputs = inputs,outputs = outputs)
        
        
@app.route('/<name>/mock_interview/analysis',methods = ['POST'])
def analysis(name):
    user = User.query.filter_by(username = name).first()
    user.is_attempting = False
    db.session.commit()
    q1id = request.form['q1']
    q2id = request.form['q2']
    q3id  = request.form['q3']
    
    q1 = Question.query.filter_by(id = q1id).first()
    q2 = Question.query.filter_by(id = q2id).first()
    q3 = Question.query.filter_by(id = q3id).first()
    
    q1s = request.form['q1s']
    q2s = request.form['q2s']
    q3s = request.form['q3s']
    
    qss = [q1s, q2s, q3s]
    qs = [q1, q2, q3]
    total = 0
    if(q1s=='true'):
        total += 15
    if(q2s == 'true'):
        total += 35
    if(q3s == 'true'):
        total += 50
    
    return render_template('mock_analysis.htm',user = user,qs = qs,
                           qss = qss,total =total )  

@app.route('/proxy')
def proxy():
    return render_template('proxy.htm')
        
if __name__ == '__main__':
    app.run(debug=True)