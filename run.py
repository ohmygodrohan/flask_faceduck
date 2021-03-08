from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import pymysql

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Heya#123@localhost/Bucketlist'
db = SQLAlchemy(app)

class Duck(db.Model):
    __tablename__='duck'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), unique=False, nullable=False)
    username = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(120), unique=False, nullable=False)
    gender = db.Column(db.String(120), unique=False, nullable=False)


@app.route('/signup',methods=['POST','GET'])
def signup():
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

@app.route('/')
def sign():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')
if __name__ == '__main__':
    app.run(debug=True)