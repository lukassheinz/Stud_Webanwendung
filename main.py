import flask_login
from flask import Flask, render_template, redirect, url_for, request, jsonify, session, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SelectField
from wtforms.validators import InputRequired, Email, Length
from database import Database
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user, login_manager
from flask_mysqldb import MySQL
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:waterslide@localhost/Studienverlaufsplan' #hier Passwort der DB und den Namen der DB eingeben
db = SQLAlchemy(app)

dbase = Database(app.config['SQLALCHEMY_DATABASE_URI'])


app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxxx!'
admin = Admin(app)
bootstrap = Bootstrap(app)


class SecureModelView(ModelView):
    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(matrikelnummer):
    return benutzer.query.get(int(matrikelnummer))

class benutzer(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    matrikelnummer = db.Column(db.Integer)
    vorname = db.Column(db.String(50))
    nachname = db.Column(db.String(50))
    email = db.Column(db.String(50), unique=True)
    passwort = db.Column(db.String(80))
    wahlvertiefung_ID = db.Column(db.Integer)
    immatrikulationssemester = db.Column(db.String(50))
    immatrikulationsjahr = db.Column(db.String(4))
    wahlvertiefung2_ID = db.Column(db.Integer)

class modul(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(50))
    modultitel = db.Column(db.String(50))
    pflicht_wahlpflicht = db.Column(db.String(50))
    empfohlen_ab = db.Column(db.Integer)
    angebotshaeufigkeit = db.Column(db.String(50))
    leistungspunkte = db.Column(db.Integer)
    semesterwochenstunden = db.Column(db.Integer)
    voraussetzungslp = db.Column(db.Integer)



class prof(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    passwort = db.Column(db.String(80))

class ProfLoginForm(FlaskForm):
    username = StringField('ID', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(min=8, max=80)])

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
                login_user(user, remember=form.remember.data)
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


@app.route('/proflogin', methods=['GET', 'POST'])
def proflogin():
    form = ProfLoginForm()
    if form.validate_on_submit():
        userx = prof.query.filter_by(ID=form.username.data).first()
        if userx:
            if userx.passwort == form.password.data:
                session['logged_in'] = True
                return redirect('/admin')
            else:
                return '<h1>Falsche Zugangsdaten</h1>'

    return render_template('proflogin.html', form=form)



admin.add_view((SecureModelView( modul, db.session)))
admin.add_view((SecureModelView( benutzer, db.session)))



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


@app.route("/modulauswahl")
#@login_required
def modulauswahl():
    user_matrikelnummer = session["matrikelnummer"]
    user_passwort_hash = session["passwort"]
    user = dbase.get_user(user_matrikelnummer, user_passwort_hash)
    user_id = session["user_ID"] = user[0][0]
    user_wahlvertiefung_ID = session["wahlvertiefung_ID"] = user[0][5]
    user_wahlvertiefung2_ID = session["wahlvertiefung2_ID"] = user[0][9]

    user_start_semester = user[0][6]
    if user_start_semester == "Wintersemester":
        start_semester = 1
    elif user_start_semester == "Sommersemester":
        start_semester = 2

    current_semester = 1

    temp = dbase.get_vertiefungen2(user_wahlvertiefung_ID)

    #Pflichtmodule Leistungspunkte
    sum_pflicht_vertiefung_lp = dbase.get_Summe_Pflicht_Vertiefung(user_wahlvertiefung_ID, user_id, current_semester)
    user_pflicht_lp_soll = temp[0][3]
    user_pflicht_lp_ist = int(sum_pflicht_vertiefung_lp[0][0])

    #Weitere Einführung Leistungspunkte
    sum_weitere_einfuherung_lp = dbase.get_Summe_weitere_Einfuehrung(user_id, current_semester)
    user_weitere_einfuehrung_LP_soll = temp[0][5]
    user_weitere_einfuehrung_LP_ist = int(sum_weitere_einfuherung_lp[0][0])

    #Grundlagenpraktikum Leistungspunkte
    sum_grundlagenpraktika_lp = dbase.get_Summe_Grundlagenpraktika(user_id, current_semester)
    user_grundlagenpraktikum_lp_soll = temp[0][4]
    user_grundlagenpraktikum_lp_ist = int(sum_grundlagenpraktika_lp[0][0])

    #Wahlpflicht Leistungspunkte
    sum_pflicht_wpf_lp = dbase.get_Summe_WPF_Vertiefung(user_id, current_semester)
    sum_wpf_andere_lp = dbase.get_Summe_WPF_andere(user_id, current_semester)
    user_min_wahlpflicht_LP = temp[0][6]
    user_max_wahlpflicht_LP = temp[0][7]
    user_wahlpflicht_LP_ist = int(sum_pflicht_wpf_lp[0][0])
    user_min_wahlpflicht_andere_LP = temp[0][8]
    user_max_wahlpflicht_andere_LP = temp[0][9]
    user_wahlpflicht_andere_LP_ist = int(sum_wpf_andere_lp[0][0])


    #LP-Gesamt
    lp_gesamt = int(dbase.get_Summe_Pflicht_Vertiefung(user_wahlvertiefung_ID, user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_Vertiefung(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_andere(user_id, current_semester)[0][0]) +\
                            int(dbase.get_Summe_Grundlagenpraktika(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_weitere_Einfuehrung(user_id, current_semester)[0][0])

    #Semesterwochenstunden
    semesterwochenstunden = int(dbase.get_Summe_Pflicht_Vertiefung_sws(user_wahlvertiefung_ID, user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_Vertiefung_sws(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_andere_sws(user_id, current_semester)[0][0]) +\
                            int(dbase.get_Summe_Grundlagenpraktika_sws(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_weitere_Einfuehrung_sws(user_id, current_semester)[0][0])

    stud = Studienverlaufsplan(1, user_wahlvertiefung_ID, user_wahlvertiefung2_ID)
    sem = Semester()
    #current_semester = current_semester + 1
    if start_semester == 1:
        current_sem = 'Sommersemester' if current_semester % 2 == 0 else 'Wintersemester'
    elif start_semester == 2:
        current_sem = 'Wintersemester' if current_semester % 2 == 0 else 'Sommersemester'

    #Pflichtmodule
    if user_pflicht_lp_ist != user_pflicht_lp_soll:
        module1 = dbase.get_module_empfohlen_pflicht(start_semester, current_semester, "Pflicht", user_id)
        pflichtkurse_nicht_empfohlen = dbase.get_module_nicht_empfohlen_pflicht(start_semester, current_semester, "Pflicht", user_id)
        pflichtkurse_vertiefung_empfohlen = dbase.get_VertiefungPflichtModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
        pflichtkurse_vertiefung_nicht_empfohlen = dbase.get_nichtEmpfohleneVertiefungPflichtModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
    else:
        module1 = []
        pflichtkurse_nicht_empfohlen = []
        pflichtkurse_vertiefung_empfohlen = []
        pflichtkurse_vertiefung_nicht_empfohlen = []
    #Grundlagenpraktikum
    if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
        if user_grundlagenpraktikum_lp_ist == 0:
            grundlagenpraktikum = dbase.get_Grundlagenpraktikum_zu_Vertiefung(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            grundlagenpraktikum_nicht_empfohlen = dbase.get_Grundlagenpraktikum_zu_Vertiefung_nicht_empfohlen(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
        else:
            grundlagenpraktikum = []
            grundlagenpraktikum_nicht_empfohlen = []
    #zweites Grundlagenmodul
    if user_weitere_einfuehrung_LP_ist != user_weitere_einfuehrung_LP_soll:
        zweites_Grundlagenmodul = dbase.get_Einfuehrung_zu_Vertiefung2(start_semester, current_semester, user_wahlvertiefung2_ID, user_id)
        zweites_Grundlagenmodul_nicht_empfohlen = dbase.get_Einfuehrung_zu_Vertiefung3(start_semester, current_semester, user_wahlvertiefung2_ID, user_id)
    #Wahlpflichtbereich
    if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
        if user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist < 30:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            if user_wahlpflicht_andere_LP_ist < 12:
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            else:
                andere_empfohlene_wahlpflichtkurse = []
                andere_nichtempfohlene_wahlpflichtkurse = []
        else:
            empfohlene_wahlpflichtkurse = []
            nichtempfohlene_wahlpflichtkurse = []
            andere_empfohlene_wahlpflichtkurse = []
            andere_nichtempfohlene_wahlpflichtkurse = []
    elif user_wahlvertiefung_ID == 2:
        if user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist < 12:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            if user_wahlpflicht_andere_LP_ist < 6:
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            else:
                andere_empfohlene_wahlpflichtkurse = []
                andere_nichtempfohlene_wahlpflichtkurse = []
        else:
            empfohlene_wahlpflichtkurse = []
            nichtempfohlene_wahlpflichtkurse = []
            andere_empfohlene_wahlpflichtkurse = []
            andere_nichtempfohlene_wahlpflichtkurse = []
    elif user_wahlvertiefung_ID == 4:
        if user_wahlpflicht_LP_ist < 6:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
        else:
            empfohlene_wahlpflichtkurse = []
            nichtempfohlene_wahlpflichtkurse = []


    gewaehlte_module = dbase.get_gewaehlte_module(user_id, current_semester)
    benutzer_modul_ids = []
    gewaehlte_module_name = []

    for i in range (len(gewaehlte_module)):
        benutzer_modul_ids.append(gewaehlte_module[i][0])
        gewaehlte_module_name.append(dbase.get_single_module(gewaehlte_module[i][4]))
    for i in gewaehlte_module_name:
        print(i)


    #TODO "Weiter"-Button soll current_semester +1 machen (Variable current_semester auf Value der Semesterliste setzen)
    if request.args.get("button_text"):
        current_semester = current_semester + 1
        print(current_semester)

    if request.is_json:
        idModule = request.args.get("value")
        id_in_benutzer_modul = request.args.get("id")
        print("ID: ", idModule)
        print(id_in_benutzer_modul)

        # Löschen aus Datenbank, wenn angeklickt
        if(request.args.get("class") == "semester-list"):
            print("class", request.args.get("class"))
            dbase.delete_belegtes_modul(id_in_benutzer_modul)
            for i in gewaehlte_module_name:
                if idModule in i:
                    gewaehlte_module_name.remove(idModule)

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
                           andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse,
                           benutzer_modul_ids = benutzer_modul_ids,
                           gewaehlte_module_name = gewaehlte_module_name,
                                   user_pflicht_lp_ist = user_pflicht_lp_ist,
                                   user_pflicht_lp_soll = user_pflicht_lp_soll,
                                   user_grundlagenpraktikum_lp_ist = user_grundlagenpraktikum_lp_ist,
                                   user_grundlagenpraktikum_lp_soll = user_grundlagenpraktikum_lp_soll,
                                   user_weitere_einfuehrung_LP_ist = user_weitere_einfuehrung_LP_ist,
                                   user_weitere_einfuehrung_LP_soll = user_weitere_einfuehrung_LP_soll,
                                   user_wahlpflicht_LP_ist = user_wahlpflicht_LP_ist,
                                   user_wahlpflicht_andere_LP_ist = user_wahlpflicht_andere_LP_ist,
                                   user_min_wahlpflicht_LP = user_min_wahlpflicht_LP,
                                   user_max_wahlpflicht_LP = user_max_wahlpflicht_LP,
                                   user_min_wahlpflicht_andere_LP = user_min_wahlpflicht_andere_LP,
                                   user_max_wahlpflicht_andere_LP = user_max_wahlpflicht_andere_LP,
                                   lp_gesamt = lp_gesamt,
                                   semesterwochenstunden = semesterwochenstunden)

        # TODO Voraussetzungen prüfen
        """
        id_list_voraussetzungen = []
        kurs_voraussetzung = dbase.get_modul_voraussetzungen(str(idModule))
        print(kurs_voraussetzung)
        for v in kurs_voraussetzung:
            if str(idModule) == str(v[2]):
                id_list_voraussetzungen.append(str(v[1]))
                for i in id_list_voraussetzungen:
                    # Bis hier sollte es funktionieren
                    #TODO Datenbankabfrage für id_list_temp_vor_sem

                    for t in id_list_temp_vor_sem:
                        if i == t:
                            break
                    else:
                        #TODO Flash für die Warnung
                        print("Kurs hat eine Voraussetzung mit der ID: " + str(i) +
                                  ", welche du noch nicht abgeschlossen hast")
        """


        elementFromDB = dbase.get_single_module(idModule)

        #Falls Wahlpflichtmodul überlassene LP übersteigt
        if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
            for i in empfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 30):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        #TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in nichtempfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 30):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                    # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in andere_empfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if(user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or(user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in andere_nichtempfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
        elif user_wahlvertiefung_ID == 2:
            for i in empfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 12):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        #TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in nichtempfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 12):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                    # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in andere_empfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if(user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 6):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass
            for i in andere_nichtempfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 6):
                        flash("Wahl des Modules mit ID " + idModule + " nicht möglich.")
                        # TODO Flash Wahl des Moduls mit ID: idModule nicht möglich
                        pass

        element = Veranstaltung(str(elementFromDB[0][0]), str(elementFromDB[0][1]), str(elementFromDB[0][2]),
                                str(elementFromDB[0][3]), str(elementFromDB[0][4]),
                                str(elementFromDB[0][5]), str(elementFromDB[0][6]), str(elementFromDB[0][7]),
                                str(elementFromDB[0][8]))
        sem.add_course(element)
        print(element)
        print(str(sem.courses))

        #Modul in benutzer_modul hinzufügen
        dbase.insert_benutzer_modul(user_id, idModule, current_semester)

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
                           andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse,
                           gewaehlte_module_name = gewaehlte_module_name,
                           benutzer_modul_ids = benutzer_modul_ids,
                               user_pflicht_lp_ist=user_pflicht_lp_ist,
                               user_pflicht_lp_soll=user_pflicht_lp_soll,
                               user_grundlagenpraktikum_lp_ist=user_grundlagenpraktikum_lp_ist,
                               user_grundlagenpraktikum_lp_soll=user_grundlagenpraktikum_lp_soll,
                               user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                               user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                               user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                               user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                               user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                               user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                               user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                               user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                               lp_gesamt = lp_gesamt,
                               semesterwochenstunden=semesterwochenstunden
                               )



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
                           andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse,
                           gewaehlte_module_name = gewaehlte_module_name,
                           benutzer_modul_ids = benutzer_modul_ids,
                               user_pflicht_lp_ist=user_pflicht_lp_ist,
                               user_pflicht_lp_soll=user_pflicht_lp_soll,
                               user_grundlagenpraktikum_lp_ist=user_grundlagenpraktikum_lp_ist,
                               user_grundlagenpraktikum_lp_soll=user_grundlagenpraktikum_lp_soll,
                               user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                               user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                               user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                               user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                               user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                               user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                               user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                               user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                               lp_gesamt = lp_gesamt,
                               semesterwochenstunden=semesterwochenstunden
                               )

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')
   # return redirect(url_for('modulauswahl'))


if __name__ == '__main__':
    app.run(debug=True)
