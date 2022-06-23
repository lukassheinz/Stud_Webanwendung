from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from database import Database
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from flask_mysqldb import MySQL

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:1nf0rmat!k@localhost/propra2022' #hier Passwort der DB und den Namen der DB eingeben
db = SQLAlchemy(app)

dbase = Database(app.config['SQLALCHEMY_DATABASE_URI'])


app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxxx!'
bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class benutzer(UserMixin, db.Model):
    matrikelnummer = db.Column(db.Integer, primary_key=True)
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    passwort = db.Column(db.String(80))
    wahlvertiefung_ID = db.Column(db.Integer)
    immatrikulationssemester = db.Column(db.String(50))
    immatrikulationsjahr = db.Column(db.String(4))
    wahlvertiefung2_ID = db.Column(db.Integer)

@login_manager.user_loader
def load_user(matrikelnummer):
    return benutzer.query.get(int(matrikelnummer))

class LoginForm(FlaskForm):
    username = StringField('Matrikelnummer', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    choices = []
    vertiefungen = dbase.get_vertiefungen()
    for vertiefung in vertiefungen:
        choices = choices + [(vertiefung[0], vertiefung[1])]

    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Matrikelnummer', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    vorname = StringField('Vorname', validators=[InputRequired(), Length(max=80)])
    nachname = StringField('Nachname', validators=[InputRequired(), Length(max=80)])
    immatrikulationssemester = SelectField('Immatrikulationssemester', choices=('Wintersemester', 'Sommersemester'))
    immatrikulationsjahr = StringField('Immatrikulationsjahr', validators=[InputRequired(), Length(min=4, max=4)])
    erste_Vertiefung = SelectField('Vertiefung 1', choices=choices) #('Embedded Systems', 'Visual Computing', 'Complex and Intelligent Software Systems', 'Medizinische Informatik'))
    zweite_Vertiefung = SelectField('Vertiefung 2', choices=choices) #('Embedded Systems', 'Visual Computing', 'Complex and Intelligent Software Systems', 'Medizinische Informatik'))

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = benutzer.query.filter_by(matrikelnummer=form.username.data).first()
        if user:
            if check_password_hash(user.passwort, form.password.data):
                #login_user(user, remember=form.remember.data)
                return redirect(url_for('verlaufsplan'))

        return '<h1>Falsche Zugangsdaten</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = benutzer(matrikelnummer=form.username.data, vorname=form.vorname.data, nachname=form.nachname.data, email=form.email.data, passwort=hashed_password, wahlvertiefung_ID=form.erste_Vertiefung.data, wahlvertiefung2_ID=form.zweite_Vertiefung.data, immatrikulationssemester=form.immatrikulationssemester.data, immatrikulationsjahr=form.immatrikulationsjahr.data)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)

@app.route('/verlaufsplan')
def verlaufsplan():
    ergebnis = dbase.get_vertiefungen()         #Beispiel - nach dbase. alle Einträge der database.py einsetzbar
    anzahl = 0
    for erg in ergebnis:
        anzahl = anzahl + 1
        print(erg)

    return render_template('verlaufsplan.html', len=anzahl, ergebnis=ergebnis)  # , name=current_user.username


if __name__ == '__main__':
    app.run(debug=True)

