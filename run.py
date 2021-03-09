from flask import Flask, render_template, request, redirect, session, url_for,flash
from flask_sqlalchemy import SQLAlchemy
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

@app.route('/')
def base():
    if 'username' in session:
        return render_template('home.html')
    else:
        return render_template('home.html')

@app.route('/logindb', methods = ['GET','POST'])
def logindb():
    if request.method == 'POST':
        name = request.form['username']
        password = request.form['password']
        data = Duck.query.filter_by(username=name,password=password).first()
        if data is not None:
            session['logged_in']=True
            session['username']= name
            return redirect(url_for('dash'))
        else:
            flash('invalid credentials')
            return redirect(url_for('login'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['logged_in'] = False
    return redirect(url_for('base'))

@app.route('/dashboard')
def dash():
    return render_template('dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)