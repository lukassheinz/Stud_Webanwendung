from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
#from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
#from nib import *

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Propra2022xyz!'
app.config['MYSQL_DB'] = 'webbenutzer'

mysql = MySQL(app)
app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxxx!'
bootstrap = Bootstrap(app)

class LoginForm(FlaskForm):
    username = StringField('Matrikelnummer', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Matrikelnummer', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    vorname = StringField('Vorname', validators=[InputRequired(), Length(max=80)])
    nachname = StringField('Nachname', validators=[InputRequired(), Length(max=80)])

listid = []
listpw = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/verlaufsplan')
def verlaufsplan():
    return render_template('verlaufsplan.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():

        matrikelnummer = form.username.data
        password = form.password.data

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * from benutzer_daten ")
        myresult = cursor.fetchall()
        for x in myresult:
            listid.append(str(x[0]))
            listpw.append(str(x[4]))

        if matrikelnummer in listid and password in listpw:
            return redirect(url_for('verlaufsplan'))
        else:
            return '<h1>Falsche Daten!!!</h1>'
    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():

        #hashed_password = generate_password_hash(form.password.data, method='sha256')
        matrikelnummer = form.username.data
        vorname = form.vorname.data
        nachname = form.nachname.data
        email = form.email.data
        password = form.password.data
        #password = hashed_password
        cursor = mysql.connection.cursor()
        cursor.execute(''' INSERT INTO benutzer_daten VALUES(%s,%s,%s,%s,%s)''',(matrikelnummer, vorname, nachname, email, password))
        mysql.connection.commit()
        cursor.close()
        #return '<h1>Neuer Benutzer wurde estellt!</h1>'
        return redirect(url_for('login'))


    return render_template('signup.html', form=form)

if __name__ == "__main__":
    app.run()
