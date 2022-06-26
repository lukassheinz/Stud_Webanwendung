import flask_login
from flask import Flask, render_template, redirect, url_for, request, jsonify, session
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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R33dxq2!!zghj@localhost/neu_studienverlaufsplan' #hier Passwort der DB und den Namen der DB eingeben
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



class Studienverlaufsplan:

    def __init__(self, start_semester, first_spec, second_spec):
        self.start_semester = 'Wintersemester' if start_semester == 1 else 'Sommersemester'
        self.first_spec = first_spec
        self.second_spec = second_spec
        self.remaining_lps = 180
        self.semesters = []

    def get_remaining_lps(self):
        return self.remaining_lps

    def decrement_lp(self, lps):
        self.remaining_lps = self.remaining_lps - lps

    def add_sem(self, sem):
        self.semesters.append(sem)

    def swap_courses(self, first, second):
        first_sem = first_course = second_sem = second_course = -1
        for i, sem in enumerate(self.semesters):
            for j, course in enumerate(sem.courses):
                if course.id == second:
                    second_sem = i
                    second_course = j
                if course.id == first:
                    first_sem = i
                    first_course = j

        if first_sem == -1:
            print("Kurs mit der ID " + str(first) + " kommt im Studienverlaufsplan nicht vor!")
            return
        if second_sem == -1:
            print("Kurs mit der ID " + str(second) + " kommt im Studienverlaufsplan nicht vor!")
            return

        sem_temp = self.semesters[second_sem].courses[second_course]
        self.semesters[second_sem].courses[second_course] = self.semesters[first_sem].courses[first_course]
        self.semesters[first_sem].courses[first_course] = sem_temp

    def check_vor(self, eingabesem):
        for i, sem in enumerate(self.semesters):
            for j, course in enumerate(sem.courses):
                if course.id == eingabesem:
                    print("test")
                    print("test")
                    print("test")
                    print("test")

    def __str__(self):
        i = 0
        st = ""
        st += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n"
        for Semester in self.semesters:
            st += "Semester " + str(i + 1) + ": \n"
            st += str(Semester)
            st += "----------------------------------------------------------------------------------------------------\n"
            i += 1
        st += "++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++"
        return st



class Semester:

    def __init__(self): #, fachsemester, WiSeSoSe):  # , cp):
        #self.fachsemester = current_sem
        # self.semesterVeranstaltungen = []
        # self.semester = WiSeSoSe
        self.courses = []
        # self.cp = cp

    # TODO Funktiion aus der main sollte hier erzeugt werden für Speicherung. Vorher Instanz von Kurs bilden
    def add_course(self, modul):
        self.courses.append(modul)

    def __str__(self):
        st = ""
        for Veranstaltung in self.courses:
            st += str(Veranstaltung) + "\n"
        return st


class Veranstaltung:
    def __init__(self, id, nummer, modultitel, pflicht_wahlpflicht, empfohlen_ab,
                 angebotshaeufigkeit, leistungspunkte, semesterwochenstunden, voraussetzungslp):
        self.id = id
        self.nummer = nummer
        self.modultitel = modultitel
        self.pflicht_wahlpflicht = pflicht_wahlpflicht
        self.empfohlen_ab = empfohlen_ab
        self.angebotshaeufigkeit = angebotshaeufigkeit
        self.leistungspunkte = leistungspunkte
        self.semesterwochenstunden = semesterwochenstunden
        self.voraussetzungslp = voraussetzungslp
        self.veranstaltung_list = [self.id, self.nummer, self.modultitel, self.pflicht_wahlpflicht,
                              self.empfohlen_ab, self.angebotshaeufigkeit, self.leistungspunkte,
                              self.semesterwochenstunden, self.voraussetzungslp]

    def __str__(self):
        return "ID: " + str(self.id) + ", Nummer: " + self.nummer + ", Modultitel: " + self.modultitel + \
               ", Pficht oder Wahlpflicht: " + self.pflicht_wahlpflicht + \
               ", Empfohlen ab: " + str(self.empfohlen_ab) + ", Angebotshäufigkeit: " + self.angebotshaeufigkeit + \
               ", Leitungspunkte: " + str(self.leistungspunkte) + ", Semesterwochenstunden: " + str(
            self.semesterwochenstunden) + \
               ", Voraussetzungslp: " + str(self.voraussetzungslp)



@login_manager.user_loader
def load_user(matrikelnummer):
    return benutzer.query.get(int(matrikelnummer))

class LoginForm(FlaskForm):
    username = StringField('Matrikelnummer', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')

class RegisterForm(FlaskForm):
    choices = [(0, "-- Bitte Vertiefung wählen --")]
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
                session["matrikelnummer"] = request.form["username"]
                session["passwort"] = user.passwort
                #login_user(user, remember=form.remember.data)
                return redirect(url_for('modulauswahl'))

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
    """
    ergebnis = dbase.get_vertiefungen()         #Beispiel - nach dbase. alle Einträge der database.py einsetzbar
    anzahl = 0
    for erg in ergebnis:
        anzahl = anzahl + 1
        print(erg)

    return render_template('index2.html', len=anzahl, ergebnis=ergebnis)  # , name=current_user.username
    """
    return render_template("verlaufsplan.html")

    return render_template('verlaufsplan.html')

wahlvertiefung_ID = 1
wahlvertiefung_ID_2 = 2
#immatrikulationssemester = "Wintersemester"
start_semester = 1 # Wintersemester


@app.route("/modulauswahl")
def modulauswahl():
    user_matrikelnummer = session["matrikelnummer"]
    user_passwort_hash = session["passwort"]
    print(user_matrikelnummer, user_passwort_hash)
    if wahlvertiefung_ID == 1:  # Embedded Systems
        pflicht_lp = 138  # muss 0 sein
        grundlagenpraktikum_lp = 0
        andereGrundlage_lp = 0
        wahlpflicht_vertiefung_lp = 0  # muss zwischen 18 und 30 sein
        andere_vertiefung_lp = 0  # muss zwischen 0 und 12 sein
    elif wahlvertiefung_ID == 2:  # Visual Computing
        pflicht_lp = 162
        andereGrundlage_lp = 0
        wahlpflicht_vertiefung_lp = 0  # muss zwischen 6 und 12 sein
        andere_vertiefung_lp = 0  # muss zwischen 0 und 6 sein
    elif wahlvertiefung_ID == 3:  # Complex and Intelligent Software Systems
        pflicht_lp = 138
        grundlagenpraktikum_lp = 0  # muss 6 sein
        andereGrundlage_lp = 0
        wahlpflicht_vertiefung_lp = 0  # muss zwischen 18 und 30 sein
        andere_vertiefung_lp = 0  # muss zwischen 0 und 12 sein
    elif wahlvertiefung_ID == 4:  # Medizinische Informatik
        pflicht_lp = 168
        andereGrundlage_lp = 0
        wahlpflicht_vertiefung_lp = 0  # muss 6 sein
        andere_vertiefung_lp = 0

    stud = Studienverlaufsplan(1, wahlvertiefung_ID, wahlvertiefung_ID_2)
    current_semester = 0
    id_list_in_semester = [] # alle module rein, um zu prüfen, ob modul bereits in einem semester drin ist

    sem = Semester()
    current_semester = current_semester + 1
    if start_semester == 1:
        current_sem = 'Sommersemester' if current_semester % 2 == 0 else 'Wintersemester'
    elif start_semester == 2:
        current_sem = 'Wintersemester' if current_semester % 2 == 0 else 'Sommersemester'

    #Pflichtmodule
    if pflicht_lp != 0:
        #TODO datenbankabfragen für alle in form von: gib alle module aus, die aber noch nicht im studienverlaufsplan sind
        module1 = dbase.get_module_empfohlen_pflicht(start_semester, current_semester, "Pflicht")
        pflichtkurse_nicht_empfohlen = dbase.get_module_nicht_empfohlen_pflicht(start_semester, current_semester, "Pflicht")
        pflichtkurse_vertiefung_empfohlen = dbase.get_VertiefungPflichtModule(start_semester, current_semester, wahlvertiefung_ID)
        pflichtkurse_vertiefung_nicht_empfohlen = dbase.get_nichtEmpfohleneVertiefungPflichtModule(start_semester, current_semester, wahlvertiefung_ID)
    #Grundlagenpraktikum
    if wahlvertiefung_ID == 1 or wahlvertiefung_ID == 3:
        if grundlagenpraktikum_lp == 0:
            grundlagenpraktikum = dbase.get_Grundlagenpraktikum_zu_Vertiefung(start_semester, current_semester, wahlvertiefung_ID)
            grundlagenpraktikum_nicht_empfohlen = dbase.get_Grundlagenpraktikum_zu_Vertiefung_nicht_empfohlen(start_semester, current_semester, wahlvertiefung_ID)
    #zweites Grundlagenmodul
    if andereGrundlage_lp == 0:
        zweites_Grundlagenmodul = dbase.get_Einfuehrung_zu_Vertiefung2(start_semester, current_semester, wahlvertiefung_ID_2)
        zweites_Grundlagenmodul_nicht_empfohlen = dbase.get_Einfuehrung_zu_Vertiefung3(start_semester, current_semester, wahlvertiefung_ID_2)
    #Wahlpflichtbereich
    if wahlvertiefung_ID == 1 or wahlvertiefung_ID == 3:
        if wahlpflicht_vertiefung_lp + andere_vertiefung_lp < 30:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, wahlvertiefung_ID)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, wahlvertiefung_ID)
            if andere_vertiefung_lp < 12:
                if wahlvertiefung_ID == 1:
                    pass
                if wahlvertiefung_ID == 3:
                    pass
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, wahlvertiefung_ID)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, wahlvertiefung_ID)
    elif wahlvertiefung_ID == 2:
        if wahlpflicht_vertiefung_lp + andere_vertiefung_lp < 12:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, wahlvertiefung_ID)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, wahlvertiefung_ID)
            if andere_vertiefung_lp < 6:
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, wahlvertiefung_ID)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, wahlvertiefung_ID)
    elif wahlvertiefung_ID == 4:
        if wahlpflicht_vertiefung_lp < 6:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, wahlvertiefung_ID)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, wahlvertiefung_ID)


    if request.args.get("button_text"):
        current_semester = current_semester + 1
        print(current_semester)

    if request.is_json:
        idModule = request.args.get("value")
        #modulText = request.args.get("text")
        selectedModules = request.args.get("selectedModules")
        print("selectedModules: ", selectedModules)
        print("ID: ", idModule)
        #TODO exception handling (flash? anstatt alert)
        if idModule in selectedModules:
            print("DUPLIKAT")
            return None
        elementFromDB = dbase.get_single_module(idModule)
        element = Veranstaltung(str(elementFromDB[0][0]), str(elementFromDB[0][1]), str(elementFromDB[0][2]),
                                str(elementFromDB[0][3]), str(elementFromDB[0][4]),
                                str(elementFromDB[0][5]), str(elementFromDB[0][6]), str(elementFromDB[0][7]),
                                str(elementFromDB[0][8]))
        sem.add_course(element)
        print(element)
        print(str(sem.courses))

        return jsonify({"ID": str(elementFromDB[0][0]),
                        "nummer": str(elementFromDB[0][1]),
                        "modultitel": str(elementFromDB[0][2]),
                        "pflicht_wahlpflicht": str(elementFromDB[0][3]),
                        "empfohlen_ab": str(elementFromDB[0][4]),
                        "angebotshaeufigkeit": str(elementFromDB[0][5]),
                        "leistungspunkte": str(elementFromDB[0][6]),
                        "semesterwochenstunden": str(elementFromDB[0][7]),
                        "voraussetzungslp": str(elementFromDB[0][8])})

        # TODO element in Datenbank einspeisen
        #dbase.insert_benutzer_modul(1, idModule, current_semester)

    #TODO Gespeicherte Module aus Datenbank in ul als li hinzufügen (get_belegte_Module(benutzer_id, semester, stud_id) oder ähnlich


    return render_template("modulauswahl.html",
                           module1=module1,
                           pflichtkurse_nicht_empfohlen=pflichtkurse_nicht_empfohlen,
                           pflichtkurse_vertiefung_empfohlen=pflichtkurse_vertiefung_empfohlen,
                           pflichtkurse_vertiefung_nicht_empfohlen=pflichtkurse_vertiefung_nicht_empfohlen,
                           grundlagenpraktikum=grundlagenpraktikum,
                           grundlagenpraktikum_nicht_empfohlen=grundlagenpraktikum_nicht_empfohlen,
                           zweites_Grundlagenmodul=zweites_Grundlagenmodul,
                           zweites_Grundlagenmodul_nicht_empfohlen=zweites_Grundlagenmodul_nicht_empfohlen,
                           empfohlene_wahlpflichtkurse=empfohlene_wahlpflichtkurse,
                           nichtempfohlene_wahlpflichtkurse=nichtempfohlene_wahlpflichtkurse,
                           andere_empfohlene_wahlpflichtkurse=andere_empfohlene_wahlpflichtkurse,
                           andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse)


if __name__ == '__main__':
    app.run(debug=True)
