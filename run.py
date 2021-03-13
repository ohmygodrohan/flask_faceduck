from flask import Flask, render_template, request, redirect, session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pymysql


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Heya#123@localhost/Bucketlist'
app.config['SECRET_KEY'] = 'ic34rv7 g7'
db = SQLAlchemy(app)

class Duck(db.Model):
    __tablename__='duck'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)

class Blog(db.Model):
    __tablename__ = 'blogpost'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120), unique=True, nullable=False)
    title = db.Column(db.String(20),nullable = False)
    date_posted = db.Column(db.DateTime,nullable = False,default=datetime.utcnow)
    content = db.Column(db.String(20),nullable = False,)

@app.route('/signupdb',methods=['POST','GET'])
def signupdb():
   if request.method == 'POST':
    _name = request.form['idname']
    _username = request.form['idusername']
    _email = request.form['idemail']
    _gender = request.form['gender']
    _password = request.form['idpassword']
    entry = Duck(email=_email,password=_password,username=_username,name=_name,gender=_gender)
    db.session.add(entry)
    db.session.commit()
    return render_template('login.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')
"""
@app.route('/')
def base():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('dashboard.html')"""

@app.route('/logindb', methods = ['GET','POST'])
def logindb():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        data = Duck.query.filter_by(username=name,password=password).first()
        if data is not None:
            session['logged_in']=True
            session['username']=name
            return redirect(url_for('dash'))
        else:
            flash('invalid credentials')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('base'))

@app.route('/')
def dash():
    post = Blog.query.order_by(Blog.date_posted.desc()).all()
    return render_template('dashboard.html',post=post)

@app.route('/blog')
def blog():
    return render_template('blog.html')


@app.route('/blogprocess', methods = ['POST','GET'])
def blogprocess():
    if request.method =='POST':
        title = request.form['title']
        content = request.form['content']
        entry = Blog(title=title,content=content,username=session['username'])
        db.session.add(entry)
        db.session.commit()
        return redirect(url_for('dash'))
    else:
        return redirect(url_for('blogprocess'))

@app.route('/mycontent')
def mycontent():
    a = Blog.query.filter(Blog.username == session['username']).order_by(Blog.date_posted.desc()).all()
    return render_template('mycontent.html',data=a)

@app.route('/blogedit', methods=['GET','POST'])
def blogedit():
    id = request.args.get('id')
    data = Blog.query.filter_by(id=id).first()

    return render_template('edit.html',data=data)


@app.route('/editblog',methods=['GET','POST'])
def blogupdate():
    if request.method == 'POST':
        item = Blog.query.get(request.form['id'])
        item.title = request.form['title']
        item.content = request.form['content']
        item.date_posted=datetime.utcnow()
        db.session.commit()
        return redirect(url_for('mycontent'))
    else:
        return "error server are busy rn"


@app.route('/delete',methods=['GET','POST'])
def deleteblog():
    Blog.query.filter_by(id=request.args.get('id')).delete()
    db.session.commit()
    return redirect(url_for('mycontent'))





if __name__ == '__main__':
    app.run(debug=True)
