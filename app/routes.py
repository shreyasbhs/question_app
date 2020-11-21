import os
from app import app
from werkzeug.datastructures import CombinedMultiDict
from flask import Flask,render_template,url_for,redirect,request,flash
from forms import (SignupForm,LoginForm,CreateQuestion,AdminForm)
from flask_login import current_user,login_user,logout_user
from models import User,Question,Admin
from app import db
import random
from compiler import compile_it


basedir = 'C:\\Users\\user\\Desktop\\web\\flask\\practise\\practise2\\question_app\\'
@app.route('/')
@app.route('/<name>')
def home(name=""):
    questions = Question.query.all()
    return render_template('home.htm',name = name,questions = questions)




@app.route('/signup',methods = ['GET','POST'])
def signup():
        
        form = SignupForm()
        if form.validate_on_submit():
            u = form
            user = User(firstname = u.firstname.data,lastname = u.lastname.data,
                    username = u.username.data,email = u.email.data, password = u.password.data)
            user.set_password(u.password.data)
            db.session.add(user)
            db.session.commit()
            flash("You have registered sucessfully!!!")
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
            flash("Invalid User name or Password")
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
            flash("Invalid User name or Password")
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
        q.inputfile.data.save(os.path.join(basedir,'io\\input\\'+ifile))
        #generate output file
        
        file = open(os.path.join(basedir,'io\\output\\'+ofile),'w')
        file.close()
        with open(os.path.join(basedir,'io\\output\\'+ofile),'w') as of:
            for line in q.output.data:
                line = line.rstrip('\n')
                of.write(line)
            of.close()
            
            
            
        que = Question(title  = q.title.data,content = q.content.data,
                      outputfile = ofile,inputfile = ifile)
       
        
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
        q.inputfile.data.save(os.path.join(basedir,'io\\input\\'+ifile))
        #generate output file
        
        file = open(os.path.join(basedir,'io\\output\\'+ofile),'w')
        file.close()
        with open(os.path.join(basedir,'io\\output\\'+ofile),'w') as of:
            for line in q.output.data:
                line = line.rstrip('\n')
                of.write(line)
            of.close()
            
            
            
        que = Question(title  = q.title.data,content = q.content.data,
                      outputfile = ofile,inputfile = ifile)
       
        
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
        fi = question.inputfile
        fo =question.outputfile
        custom_o_file = open(os.path.join(basedir,'io\\output\\'+fo),'r')
        custom_i_file = open(os.path.join(basedir,'io\\input\\'+fi),'r')
        customoutput = custom_o_file.read()
        custominput = custom_i_file.read()
        if request.method == 'POST':
            code = request.form['code']
            inp = request.form['inp']
            # result = compile_it(code,inp)
            return render_template('problem.htm',result = result,code = code,
                                   inp = inp,question = question,id = question.id,
                                   customout=customoutput,custominput = custominput)
        else:
            
            return render_template('problem.htm',result = "",code = "",
                                   inp = "",question = question,id = question.id
                                   ,customoutput = customoutput,custominput = custominput);


@app.route('/mock_interview/<name>',methods = ['GET','POST'])
def mock_interview(name):
    
    if(request.method=="POST"):
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
        custom_o_file = open(os.path.join(basedir,'io\\output\\'+fo),'r')
        custom_i_file = open(os.path.join(basedir,'io\\input\\'+fi),'r')
        customoutput = custom_o_file.read()
        custominput = custom_i_file.read()
        inputs.append(custominput)
        outputs.append(customoutput)
   
    return render_template('mock_interview.htm',name = name,q1 = q1,q2 = q2,q3 = q3,inputs = inputs,outputs = outputs)
    


    
        
if __name__ == '__main__':
    app.run(debug=True)