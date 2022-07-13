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

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:R33dxq2!!zghj@localhost/neu_studienverlaufsplan' #hier Passwort der DB und den Namen der DB eingeben
db = SQLAlchemy(app)

dbase = Database(app.config['SQLALCHEMY_DATABASE_URI'])


app.config['SECRET_KEY'] = 'xxxxxxxxxxxxxxxxx!'
admin = Admin(app, template_mode='bootstrap4', name='Verwaltung')
bootstrap = Bootstrap(app)


class SecureModelViewModul(ModelView):
    # can_delete = False  # disable model deletion
    page_size = 100  # the number of entries to display on the list view
    #create_modal = True
    #edit_modal = True

    edit_template = 'modul_edit.html'
    create_template = 'modul_create.html'

    form_excluded_columns = ['modulvertiefung']

    form_choices = {
        ####### Für Module
        'pflicht_wahlpflicht': [('Pflicht', 'Pflicht'), ('Wahlpflicht', 'Wahlpflicht'), ('Einfuehrung', 'Einfuehrung'),
                                ('Grundlagenpraktikum', 'Grundlagenpraktikum')],
        'empfohlen_ab': [('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6')],
        'angebotshaeufigkeit': [('Wintersemester', 'Wintersemester'), ('Sommersemester', 'Sommersemester'),
                                ('Wintersemester, Sommersemester', 'Wintersemester, Sommersemester')]
    }

    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    def get_save_return_url(self, model, is_created=False):
        return url_for('Vertiefung.create_view')

class SecureModelViewBenutzer(ModelView):
    # can_delete = False  # disable model deletion
    page_size = 100  # the number of entries to display on the list view
    #create_modal = True
    #edit_modal = True

    edit_template = 'benutzer_edit.html'
    create_template = 'benutzer_create.html'



    form_choices = {
        'wahlvertiefung_ID': [('1', 'Embedded Systems'), ('2', 'Visual Computing'),
                              ('3', 'Complex and Intelligent Software Systems'), ('4', 'Medizinische Informatik')],
        'wahlvertiefung2_ID': [('1', 'Embedded Systems'), ('2', 'Visual Computing'),
                               ('3', 'Complex and Intelligent Software Systems'), ('4', 'Medizinische Informatik')],
        'immatrikulationssemester': [('Wintersemester', 'Wintersemester'), ('Sommersemester', 'Sommersemester')]
    }

    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    def get_save_return_url(self, model, is_created=False):
        return url_for('Modul.create_view')


class SecureModelViewVoraussetzung(ModelView):
    # can_delete = False  # disable model deletion
    page_size = 100  # the number of entries to display on the list view
    #create_modal = True
    #edit_modal = True

    #edit_template = 'benutzer_edit.html'
    create_template = 'Voraussetzung_create.html'

    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    def get_save_return_url(self, model, is_created=False):
        return url_for('admin.index')

class SecureModelViewVertiefung(ModelView):
    # can_delete = False  # disable model deletion
    page_size = 100  # the number of entries to display on the list view
    #create_modal = True
    #edit_modal = True

    #edit_template = 'benutzer_edit.html'
    create_template = 'vertiefung_create.html'


    def is_accessible(self):
        if "logged_in" in session:
            return True
        else:
            abort(403)

    def get_save_return_url(self, model, is_created=False):
        return url_for('Voraussetzung.create_view')



login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'



@login_manager.user_loader
def load_user(matrikelnummer):
    return Studierende.query.get(int(matrikelnummer))

class Studierende(UserMixin, db.Model):
    __tablename__ = 'benutzer'
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

class Modul(UserMixin, db.Model):
    __tablename__ = 'modul'
    ID = db.Column(db.Integer, primary_key=True)
    nummer = db.Column(db.String(50))
    modultitel = db.Column(db.String(50))
    pflicht_wahlpflicht = db.Column(db.String(50))
    empfohlen_ab = db.Column(db.Integer)
    angebotshaeufigkeit = db.Column(db.String(50))
    leistungspunkte = db.Column(db.Integer)
    semesterwochenstunden = db.Column(db.Integer)
    voraussetzungslp = db.Column(db.Integer)
    modulvertiefung = db.relationship('Modulvertiefung', backref='modul')
    def __str__(self):
        return self.modultitel

class Vertiefung(UserMixin, db.Model):
    __tablename__ = 'vertiefung'
    ID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    prof_ID = db.Column(db.Integer)
    pflicht_LP = db.Column(db.Integer)
    grundlagenpraktikum_LP = db.Column(db.Integer)
    weitere_einfuehrung_LP = db.Column(db.Integer)
    min_wahlpflicht_vertiefung_LP = db.Column(db.Integer)
    max_wahlpflicht_vertiefung_LP = db.Column(db.Integer)
    min_wahlpflicht_andere_LP = db.Column(db.Integer)
    max_wahlpflicht_andere_LP = db.Column(db.Integer)
    wahlpflicht_LP = db.Column(db.Integer)
    modulvertiefung = db.relationship('Modulvertiefung', backref='vertiefung')
    def __str__(self):
        return self.name

class Modulvertiefung(UserMixin, db.Model):
    __tablename__ = 'vertiefung_modul'
    ID = db.Column(db.Integer, primary_key=True)
    vertiefung_ID = db.Column(db.Integer, db.ForeignKey('vertiefung.ID'))
    modul_ID = db.Column(db.Integer, db.ForeignKey('modul.ID'))
    zuordnung = db.Column(db.Enum('erlaubt_in', 'gehoert_zu', 'Pflicht_in'))

class Modulvoraussetzung(UserMixin, db.Model):
    __tablename__ = 'voraussetzung_modul'
    ID = db.Column(db.Integer, primary_key=True)
    modulvoraussetzung_ID = db.Column(db.Integer, db.ForeignKey('modul.ID'))
    modul_ID = db.Column(db.Integer, db.ForeignKey('modul.ID'))
    modul = db.relationship('Modul',  foreign_keys=modul_ID) #backref='modulvoraussetzung_modul',
    modulvoraussetzung = db.relationship('Modul', foreign_keys=modulvoraussetzung_ID)  #, backref='modul_voraussetzungmodul'


admin.add_view((SecureModelViewModul(Modul, db.session, endpoint='Modul')))
admin.add_view((SecureModelViewVertiefung(Modulvertiefung, db.session, endpoint='Vertiefung')))
admin.add_view((SecureModelViewVoraussetzung(Modulvoraussetzung, db.session, endpoint='Voraussetzung')))
admin.add_view((SecureModelViewBenutzer(Studierende, db.session, endpoint='Benutzer')))



class prof(UserMixin, db.Model):
    ID = db.Column(db.Integer, primary_key=True)
    passwort = db.Column(db.String(80))

class ProfLoginForm(FlaskForm):
    username = StringField('ID', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Passwort', validators=[InputRequired(), Length(max=80)])

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

@app.route('/', methods = ["GET", "POST"])
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = Studierende.query.filter_by(matrikelnummer=form.username.data).first()
        if user:
            if check_password_hash(user.passwort, form.password.data):
                session["matrikelnummer"] = request.form["username"]
                session["passwort"] = user.passwort
                session["swap_module"] = []
                login_user(user, remember=form.remember.data)
                return redirect(url_for('modulauswahl'))

        return '<h1>Falsche Zugangsdaten</h1>'

    return render_template('login.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = Studierende(matrikelnummer=form.username.data, vorname=form.vorname.data, nachname=form.nachname.data, email=form.email.data, passwort=hashed_password, wahlvertiefung_ID=form.erste_Vertiefung.data, wahlvertiefung2_ID=form.zweite_Vertiefung.data, immatrikulationssemester=form.immatrikulationssemester.data, immatrikulationsjahr=form.immatrikulationsjahr.data)
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






@app.route('/verlaufsplan', methods=["GET", "POST"])
@login_required
def verlaufsplan():
    user_matrikelnummer = session["matrikelnummer"]
    user_passwort_hash = session["passwort"]
    user = dbase.get_user(user_matrikelnummer, user_passwort_hash)
    user_id = session["user_ID"] = user[0][0]
    semester_anzahl = user[0][11]
    user_wahlvertiefung_ID = user[0][5]
    user_start_semester = user[0][6]
    semester_modul_liste = []

    if request.is_json:

        # von belegt auf abgeschlossen ändern
        if request.args.get("value") and "belegt" in request.args.get("class"):
            temp_module_id = request.args.get("value")
            semester_von_modul = request.args.get("semester")
            dbase.update_benutzer_modul(user_id, temp_module_id, semester_von_modul)

        # von abgeschlossen auf belegt ändern
        elif request.args.get("value") and "abgeschlossen" in request.args.get("class"):
            temp_module_id = request.args.get("value")
            semester_von_modul = request.args.get("semester")
            dbase.update_benutzer_modul_belegt(user_id, temp_module_id, semester_von_modul)

    #Gewählte Module bekommen
    for i in range(1, semester_anzahl + 1):
        semester_modul_liste.append(dbase.get_gewaehlte_module(user_id, i))
    module_for_jeweiliges_semester = []
    # Get gewählte Module
    for i in range(1, semester_anzahl + 1):
        module_for_jeweiliges_semester.append(dbase.get_ausgewählte_module_infos(user_id, i))

    #Für jeweiliges Semester LP und SWS bekommen
    semester_lp_liste = []
    semester_sws_liste = []
    for i in range(1, semester_anzahl + 1):
        lp_gesamt = int(dbase.get_Summe_Pflicht_Vertiefung(user_id, user_id, i)[0][0]) + \
                    int(dbase.get_Summe_WPF_Vertiefung(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_WPF_andere(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_Grundlagenpraktika(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_weitere_Einfuehrung(user_id, i)[0][0])

        semesterwochenstunden = int(dbase.get_Summe_Pflicht_Vertiefung_sws(user_id, user_id, i)[0][0]) + \
                                int(dbase.get_Summe_WPF_Vertiefung_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_WPF_andere_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_Grundlagenpraktika_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_weitere_Einfuehrung_sws(user_id, i)[0][0])

        semester_lp_liste.append(lp_gesamt)
        semester_sws_liste.append(semesterwochenstunden)

    print(semester_sws_liste)
    print(semester_lp_liste)


    return render_template("verlaufsplan.html",
                           semester_anzahl = semester_anzahl,
                           semester_modul_liste = semester_modul_liste,
                           module_for_jeweiliges_semester = module_for_jeweiliges_semester,
                           semester_lp_liste = semester_lp_liste,
                           semester_sws_liste = semester_sws_liste,
                           user_start_semester = user_start_semester)



@app.route("/swap", methods=["GET"])
@login_required
def swap():
    user_matrikelnummer = session["matrikelnummer"]
    user_passwort_hash = session["passwort"]
    user = dbase.get_user(user_matrikelnummer, user_passwort_hash)
    user_id = session["user_ID"] = user[0][0]
    semester_anzahl = user[0][11]
    semester_modul_liste = []
    user_start_semester = user[0][6]
    failed = 0


    # Gewählte Module bekommen
    for i in range(1, semester_anzahl + 1):
        semester_modul_liste.append(dbase.get_gewaehlte_module(user_id, i))
    module_for_jeweiliges_semester = []
    # Get gewählte Module
    for i in range(1, semester_anzahl + 1):
        module_for_jeweiliges_semester.append(dbase.get_ausgewählte_module_infos(user_id, i))

    # Für jeweiliges Semester LP und SWS bekommen
    semester_lp_liste = []
    semester_sws_liste = []
    for i in range(1, semester_anzahl + 1):
        lp_gesamt = int(dbase.get_Summe_Pflicht_Vertiefung(user_id, user_id, i)[0][0]) + \
                    int(dbase.get_Summe_WPF_Vertiefung(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_WPF_andere(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_Grundlagenpraktika(user_id, i)[0][0]) + \
                    int(dbase.get_Summe_weitere_Einfuehrung(user_id, i)[0][0])

        semesterwochenstunden = int(dbase.get_Summe_Pflicht_Vertiefung_sws(user_id, user_id, i)[0][0]) + \
                                int(dbase.get_Summe_WPF_Vertiefung_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_WPF_andere_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_Grundlagenpraktika_sws(user_id, i)[0][0]) + \
                                int(dbase.get_Summe_weitere_Einfuehrung_sws(user_id, i)[0][0])

        semester_lp_liste.append(lp_gesamt)
        semester_sws_liste.append(semesterwochenstunden)

    if request.is_json:
        if request.args.get("value"):

            temp_module_id = request.args.get("value")

            if str(temp_module_id) in session["swap_module"]:
                for i in session["swap_module"]:
                    if str(temp_module_id) == i:
                        session["swap_module"].remove(i)
            elif str(temp_module_id) not in session["swap_module"]:
                if len(session["swap_module"]) == 2:
                    flash("Du hast bereits 2 Module ausgewählt.")
                    return redirect(request.url)
                session["swap_module"].append(temp_module_id)

            if len(session["swap_module"]) == 2:
                swap_modul_1 = dbase.get_gewaehltes_modul(user_id, str(session["swap_module"][0]))
                swap_modul_2 = dbase.get_gewaehltes_modul(user_id, str(session["swap_module"][1]))
                swap_modul_1_info = dbase.get_single_module(str(session["swap_module"][0]))
                swap_modul_2_info = dbase.get_single_module(str(session["swap_module"][1]))
                semester_swap_modul_1 = swap_modul_1[0][2]
                semester_swap_modul_2 = swap_modul_2[0][2]

                if swap_modul_1_info[0][2] == "Bachelorarbeit" or swap_modul_2_info[0][2] == "Bachelorarbeit":
                    lp_gesamt_vor_sem_modul_1 = int(dbase.get_Summe_Pflicht_Vertiefung_Vor(user_id, user_id, semester_swap_modul_1)[0][0]) + \
                                                int(dbase.get_Summe_WPF_Vertiefung_Vor(user_id, semester_swap_modul_1)[0][0]) + \
                                                int(dbase.get_Summe_WPF_andere_Vor(user_id, semester_swap_modul_1)[0][0]) + \
                                                int(dbase.get_Summe_Grundlagenpraktika_Vor(user_id, semester_swap_modul_1)[0][0]) + \
                                                int(dbase.get_Summe_weitere_Einfuehrung_Vor(user_id, semester_swap_modul_1)[0][0])

                    lp_gesamt_vor_sem_modul_2 = int(dbase.get_Summe_Pflicht_Vertiefung_Vor(user_id, user_id, semester_swap_modul_2)[0][0]) + \
                                                int(dbase.get_Summe_WPF_Vertiefung_Vor(user_id, semester_swap_modul_2)[0][0]) + \
                                                int(dbase.get_Summe_WPF_andere_Vor(user_id, semester_swap_modul_2)[0][0]) + \
                                                int(dbase.get_Summe_Grundlagenpraktika_Vor(user_id, semester_swap_modul_2)[0][0]) + \
                                                int(dbase.get_Summe_weitere_Einfuehrung_Vor(user_id, semester_swap_modul_2)[0][0])

                    if lp_gesamt_vor_sem_modul_1 < 120 or lp_gesamt_vor_sem_modul_2 < 120:
                        flash("Tauschen nicht möglich, da Voraussetzung für die Bachleorarbeit 120LP sind.")
                        return redirect("")

                if(int(semester_swap_modul_1) == int(semester_swap_modul_2)):
                    flash("Beide Module liegen im gleichen Semester")
                    return redirect("")

                if (swap_modul_1_info[0][5] != swap_modul_2_info[0][5]): # WiSe != SoSe
                    if (swap_modul_1_info[0][5] == "Wintersemester, Sommersemester") or (swap_modul_2_info[0][5] == "Wintersemester, Sommersemester"):
                        pass
                    else:
                        flash("Die Module werden ausschließlich in unterschiedlichen Semestern (SoSe/WiSe) angeboten.")
                        return redirect("")

                # Voraussetzungen prüfen für Modul swap_modul_1 in semester von swap_modul_2
                id_list_temp_vor_sem = dbase.get_vorherige_belegte_modul_ids(user_id, semester_swap_modul_2)
                id_list_temp_vor_sem_temp = []
                unbelegte_vorausgesetzte_kurse = []
                for i in id_list_temp_vor_sem:
                    id_list_temp_vor_sem_temp.append(i[0])  # bereits belegte module (id)
                increment = 0
                kurs_voraussetzung = dbase.get_modul_voraussetzungen(str(session["swap_module"][0]))  # Voraussetzungen für idModule
                for v in kurs_voraussetzung:
                    if str(session["swap_module"][0]) == str(v[2]) and int(
                            v[1]) not in id_list_temp_vor_sem_temp:  # wenn idModule == modulID in voraussetzung_module
                        unbelegte_vorausgesetzte_kurse.append(str(v[1]))  # Vorausgesetzter kurs und noch nicht belegt
                        if unbelegte_vorausgesetzte_kurse:
                            for unbelegt in unbelegte_vorausgesetzte_kurse:
                                modul_from_db = dbase.get_single_module(unbelegt)
                                flash("Das Modul >>" + modul_from_db[0][2] + "<< wird als Voraussetzung für das Modul >>" + swap_modul_1_info[0][2] + "<< benötigt.")
                            increment = increment + 1
                            failed = failed + 1
                if increment > 0:
                    return redirect("")

                # Voraussetzungen prüfen für Modul swap_modul_2 in semester von swap_modul_1
                id_list_temp_vor_sem = dbase.get_vorherige_belegte_modul_ids(user_id, semester_swap_modul_1)
                id_list_temp_vor_sem_temp = []
                unbelegte_vorausgesetzte_kurse = []
                for i in id_list_temp_vor_sem:
                    id_list_temp_vor_sem_temp.append(i[0])  # bereits belegte module (id)
                increment = 0
                kurs_voraussetzung = dbase.get_modul_voraussetzungen(str(session["swap_module"][1]))  # Voraussetzungen für idModule
                for v in kurs_voraussetzung:
                    if str(session["swap_module"][1]) == str(v[2]) and int(
                            v[1]) not in id_list_temp_vor_sem_temp:  # wenn idModule == modulID in voraussetzung_module
                        unbelegte_vorausgesetzte_kurse.append(str(v[1]))  # Vorausgesetzter kurs und noch nicht belegt
                        if unbelegte_vorausgesetzte_kurse:
                            for unbelegt in unbelegte_vorausgesetzte_kurse:
                                modul_from_db = dbase.get_single_module(unbelegt)
                                flash("Das Modul >>" + modul_from_db[0][2] + "<< wird als Voraussetzung für das Modul >>" + swap_modul_2_info[0][2] + "<< benötigt.")
                            increment = increment + 1
                            failed = failed + 1
                if increment > 0:
                    return redirect("")

                # Voraussetzungen nachher prüfen für Modul swap_modul_1 in semester von swap_modul_2

                gewählte_module = dbase.get_alle_gewaehlte_module(user_id)
                gewählte_module_liste = []

                temp_m = []
                increment = 0

                for i in gewählte_module:
                    gewählte_module_liste.append(i[0])
                modulvoraussetzungs_IDs = dbase.get_modul_voraussetzungen_nach(str(session["swap_module"][0]))
                for v in modulvoraussetzungs_IDs:
                    if v[2] in gewählte_module_liste:
                        list_semester_voraussetzungen = []
                        temp_m.append(v[2])
                        for i in temp_m:
                            l = dbase.get_semester_of_module(user_id, i)
                            if l:
                                list_semester_voraussetzungen.append(l[0][0])

                        for i in list_semester_voraussetzungen:
                            if semester_swap_modul_2 > i:
                                vor_modul = dbase.get_single_module(v[2])
                                flash("Das Modul >>" + vor_modul[0][2] + "<< benötigt das Modul >>" + swap_modul_1_info[0][2] + "<< als Voraussetzung.")
                                increment = increment + 1
                                failed = failed + 1
                if increment > 0:
                    return redirect("")

                # Voraussetzungen nachher prüfen für Modul swap_modul_2 in semester von swap_modul_1
                temp_m = []
                increment = 0

                for i in gewählte_module:
                    gewählte_module_liste.append(i[0])
                modulvoraussetzungs_IDs = dbase.get_modul_voraussetzungen_nach(str(session["swap_module"][1]))
                for v in modulvoraussetzungs_IDs:
                    if v[2] in gewählte_module_liste:
                        list_semester_voraussetzungen = []
                        temp_m.append(v[2])
                        for i in temp_m:
                            l = dbase.get_semester_of_module(user_id, i)
                            if l:
                                list_semester_voraussetzungen.append(l[0][0])

                        for i in list_semester_voraussetzungen:
                            if semester_swap_modul_1 > i:
                                vor_modul = dbase.get_single_module(v[2])
                                flash("Das Modul >>" + vor_modul[0][2] + "<< benötigt das Modul >>" + swap_modul_2_info[0][2] + "<< als Voraussetzung.")
                                increment = increment + 1
                                failed = failed + 1
                if increment > 0:
                    return redirect("")

                if failed is 0:
                    swap_mod_1 = swap_modul_1[0][2]
                    swap_mod_2 = swap_modul_2[0][2]
                    dbase.update_semester(swap_mod_2, user_id, swap_modul_1[0][4])
                    dbase.update_semester(swap_mod_1, user_id, swap_modul_2[0][4])
                    session["swap_module"].clear()

    return render_template("swap.html",
                           semester_anzahl=semester_anzahl,
                           semester_modul_liste=semester_modul_liste,
                           module_for_jeweiliges_semester=module_for_jeweiliges_semester,
                           semester_lp_liste=semester_lp_liste,
                           semester_sws_liste=semester_sws_liste,
                           swap_module=session["swap_module"],
                           user_start_semester = user_start_semester)


@app.route("/modulauswahl", methods=["GET"])
@login_required
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
    current_semester = user[0][10]
    semester_anzahl = user[0][11]

    if request.is_json:
        if (request.args.get("class") == "semester"):
            new_current_semester = request.args.get("id")
            current_semester = new_current_semester
            dbase.update_current_semester(user_id, new_current_semester)
            return "yes"
        if (request.args.get("class") == "btn btn-primary add"):
            semester_anzahl = semester_anzahl + 1
            dbase.update_semester_anzahl(user_id, semester_anzahl)
        if (request.args.get("class") == "btn btn-warning delete"):
            if semester_anzahl > 6:
                dbase.delete_gewählte_module_in_semester(user_id, semester_anzahl)
                if semester_anzahl == current_semester:
                    current_semester = current_semester - 1
                semester_anzahl = semester_anzahl - 1
                #dbase.delete_gewählte_module_in_semester(user_id, semester_anzahl)
                dbase.update_semester_anzahl(user_id, semester_anzahl)
                dbase.update_current_semester(user_id, current_semester)
            else:
                flash("Du solltest mindestens 6 Semester studieren.")
                return redirect(request.url)

    temp = dbase.get_vertiefungen2(user_wahlvertiefung_ID)

    #Pflichtmodule Leistungspunkte
    sum_pflicht_vertiefung_lp = dbase.get_Summe_Pflicht_Vertiefung_Gesamt(user_id, user_id)
    user_pflicht_lp_soll = temp[0][3]
    user_pflicht_lp_ist = int(sum_pflicht_vertiefung_lp[0][0])

    #Weitere Einführung Leistungspunkte
    sum_weitere_einfuherung_lp = dbase.get_Summe_weitere_Einfuehrung_Gesamt(user_id)
    user_weitere_einfuehrung_LP_soll = temp[0][5]
    user_weitere_einfuehrung_LP_ist = int(sum_weitere_einfuherung_lp[0][0])

    #Grundlagenpraktikum Leistungspunkte
    sum_grundlagenpraktika_lp = dbase.get_Summe_Grundlagenpraktika_Gesamt(user_id)
    user_grundlagenpraktikum_lp_soll = temp[0][4]
    user_grundlagenpraktikum_lp_ist = int(sum_grundlagenpraktika_lp[0][0])

    #Wahlpflicht Leistungspunkte
    sum_pflicht_wpf_lp = dbase.get_Summe_WPF_Vertiefung_Gesamt(user_id)
    sum_wpf_andere_lp = dbase.get_Summe_WPF_andere_Gesamt(user_id)
    user_min_wahlpflicht_LP = temp[0][6]
    user_max_wahlpflicht_LP = temp[0][7]
    user_wahlpflicht_LP_ist = int(sum_pflicht_wpf_lp[0][0])
    user_min_wahlpflicht_andere_LP = temp[0][8]
    user_max_wahlpflicht_andere_LP = temp[0][9]
    user_wahlpflicht_andere_LP_ist = int(sum_wpf_andere_lp[0][0])
    user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist


    #LP-Gesamt
    lp_gesamt = int(dbase.get_Summe_Pflicht_Vertiefung(user_id, user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_Vertiefung(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_andere(user_id, current_semester)[0][0]) +\
                            int(dbase.get_Summe_Grundlagenpraktika(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_weitere_Einfuehrung(user_id, current_semester)[0][0])

    #LP-Gesamt in den vorherigen Semestern (Für Bachelorarbeit relevant)
    lp_gesamt_vor_sem = int(dbase.get_Summe_Pflicht_Vertiefung_Vor(user_id, user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_Vertiefung_Vor(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_andere_Vor(user_id, current_semester)[0][0]) +\
                            int(dbase.get_Summe_Grundlagenpraktika_Vor(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_weitere_Einfuehrung_Vor(user_id, current_semester)[0][0])

    lp_gesamt_alle_semester = int(dbase.get_Gesamtsumme_LP(user_id)[0][0])

    #Semesterwochenstunden
    semesterwochenstunden = int(dbase.get_Summe_Pflicht_Vertiefung_sws(user_id, user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_Vertiefung_sws(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_WPF_andere_sws(user_id, current_semester)[0][0]) +\
                            int(dbase.get_Summe_Grundlagenpraktika_sws(user_id, current_semester)[0][0]) + \
                            int(dbase.get_Summe_weitere_Einfuehrung_sws(user_id, current_semester)[0][0])


    if start_semester == 1:
        current_sem = 'Sommersemester' if current_semester % 2 == 0 else 'Wintersemester'
    elif start_semester == 2:
        current_sem = 'Wintersemester' if current_semester % 2 == 0 else 'Sommersemester'

    #Pflichtmodule
    if user_pflicht_lp_ist != user_pflicht_lp_soll:
        module1 = dbase.get_module_empfohlen_pflicht(start_semester, current_semester, "Pflicht", user_id)
        if lp_gesamt_vor_sem < 120:
            for i in module1:
                if i[2] == "Bachelorarbeit":
                    module1.remove(i)
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
    else:
        zweites_Grundlagenmodul = []
        zweites_Grundlagenmodul_nicht_empfohlen = []
    #Wahlpflichtbereich
    if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
        if user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist < 30:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            if user_wahlpflicht_andere_LP_ist < 12:
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "empfohlen_in",user_wahlvertiefung_ID, user_id)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "empfohlen_in",user_wahlvertiefung_ID, user_id)
                andere_erlaubte_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "erlaubt_in",user_wahlvertiefung_ID, user_id)
                andere_nichterlaubte_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "erlaubt_in", user_wahlvertiefung_ID, user_id)
                andere_ausgegraute_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "nicht_empfohlen_in",user_wahlvertiefung_ID, user_id)
                andere_n_ausgegraute_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "nicht_empfohlen_in", user_wahlvertiefung_ID, user_id)
            else:
                andere_empfohlene_wahlpflichtkurse = []
                andere_nichtempfohlene_wahlpflichtkurse = []
                andere_erlaubte_wahlpflichtkurse = []
                andere_nichterlaubte_wahlpflichtkurse = []
                andere_ausgegraute_wahlpflichtkurse = []
                andere_n_ausgegraute_wahlpflichtkurse = []
        else:
            empfohlene_wahlpflichtkurse = []
            nichtempfohlene_wahlpflichtkurse = []
            andere_empfohlene_wahlpflichtkurse = []
            andere_nichtempfohlene_wahlpflichtkurse = []
            andere_erlaubte_wahlpflichtkurse = []
            andere_nichterlaubte_wahlpflichtkurse = []
            andere_ausgegraute_wahlpflichtkurse = []
            andere_n_ausgegraute_wahlpflichtkurse = []
    elif user_wahlvertiefung_ID == 2:
        if user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist < 12:
            empfohlene_wahlpflichtkurse = dbase.get_VertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneVertiefungModule(start_semester, current_semester, user_wahlvertiefung_ID, user_id)
            if user_wahlpflicht_andere_LP_ist < 6:
                andere_empfohlene_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "empfohlen_in", user_wahlvertiefung_ID, user_id)
                andere_nichtempfohlene_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "empfohlen_in", user_wahlvertiefung_ID, user_id)
                andere_erlaubte_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "erlaubt_in", user_wahlvertiefung_ID, user_id)
                andere_nichterlaubte_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "erlaubt_in", user_wahlvertiefung_ID, user_id)
                andere_ausgegraute_wahlpflichtkurse = dbase.get_andereModule(start_semester, current_semester, "nicht_empfohlen_in", user_wahlvertiefung_ID, user_id)
                andere_n_ausgegraute_wahlpflichtkurse = dbase.get_nichtEmpfohleneAndereModule(start_semester, current_semester, "nicht_empfohlen_in", user_wahlvertiefung_ID, user_id)
            else:
                andere_empfohlene_wahlpflichtkurse = []
                andere_nichtempfohlene_wahlpflichtkurse = []
                andere_erlaubte_wahlpflichtkurse = []
                andere_nichterlaubte_wahlpflichtkurse = []
                andere_ausgegraute_wahlpflichtkurse = []
                andere_n_ausgegraute_wahlpflichtkurse = []
        else:
            empfohlene_wahlpflichtkurse = []
            nichtempfohlene_wahlpflichtkurse = []
            andere_empfohlene_wahlpflichtkurse = []
            andere_nichtempfohlene_wahlpflichtkurse = []
            andere_erlaubte_wahlpflichtkurse = []
            andere_nichterlaubte_wahlpflichtkurse = []
            andere_ausgegraute_wahlpflichtkurse = []
            andere_n_ausgegraute_wahlpflichtkurse = []
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

    temp_zip = zip(gewaehlte_module_name, benutzer_modul_ids)
    temp_list = list(temp_zip)

    if request.is_json:
        idModule = request.args.get("value")
        id_in_benutzer_modul = request.args.get("id")
        print("ID: ", idModule)
        print(id_in_benutzer_modul)

        # Löschen aus Datenbank, wenn angeklickt
        if(request.args.get("class") == "semester-list"):
            print("class", request.args.get("class"))

            # prüfen, ob Modul abgeschlossen ist. Falls ja, dann ist Löschen nicht mehr möglich.
            temp_modul = dbase.get_modul_from_benutzer_modul(user_id, idModule)
            if temp_modul[0][1] == "abgeschlossen":
                flash("Das Modul ist bereits abgeschlossen und kann nicht entfernt werden.")
                return redirect(request.url)

            # prüfen, ob löschung möglich ist (voraussetzungen aus nachfolgenden semestern prüfen)
            # Voraussetzungen nachher prüfen
            id_list_nachfolgende_semester = dbase.get_nachfolgende_belegte_modul_ids(user_id, current_semester)
            increment = 0
            id_list_voraussetzungen_nach = []
            modulvoraussetzungs_IDs = dbase.get_modul_voraussetzungen_nach(str(idModule))
            for v in modulvoraussetzungs_IDs:
                if str(idModule) == str(v[1]):
                    id_list_voraussetzungen_nach.append(str(v[2]))  #modul_id
                    for t in id_list_nachfolgende_semester:
                        for i in id_list_voraussetzungen_nach:
                            if int(i) == int(t[0]):
                                modul_from_db = dbase.get_single_module(i)
                                #flash("Kurs hat eine Voraussetzung mit der ID " + str(i) + " (" + modul_from_db[0][2] + ") , welche den Kurs als voraussetzung in einem folgenden Semester hat.")
                                flash("Das Modul kann nicht abgewählt werden, weil der Kurs >>" + modul_from_db[0][2] + "<<, welches in einem späteren Semester gewählt wurde, das Modul als Voraussetzung hat.")
                                #print("Kurs hat eine Voraussetzung mit der ID " + str(i) + ", welche den Kurs als voraussetzung in einem folgenden Semester hat.")
                                increment = increment + 1
            if increment > 0:
                return redirect(request.url)

            dbase.delete_belegtes_modul(id_in_benutzer_modul)

            for i in gewaehlte_module_name:
                if idModule in i:
                    gewaehlte_module_name.remove(idModule)

            return render_template("modulauswahl.html",
                           module1=module1,
                           user_start_semester=user_start_semester,
                           user_wahlvertiefung_ID=user_wahlvertiefung_ID,
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
                                   semesterwochenstunden = semesterwochenstunden,
                                   temp_list = temp_list,
                                   lp_gesamt_alle_semester = lp_gesamt_alle_semester,
                                   current_semester = current_semester,
                                   user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist_summe,
                                   semester_anzahl = semester_anzahl,
                                   andere_erlaubte_wahlpflichtkurse=andere_erlaubte_wahlpflichtkurse,
                                   andere_nichterlaubte_wahlpflichtkurse=andere_nichterlaubte_wahlpflichtkurse,
                                   andere_ausgegraute_wahlpflichtkurse=andere_ausgegraute_wahlpflichtkurse,
                                   andere_n_ausgegraute_wahlpflichtkurse=andere_n_ausgegraute_wahlpflichtkurse
                                   )



        # Voraussetzungen prüfen
        id_list_temp_vor_sem = dbase.get_vorherige_belegte_modul_ids(user_id, current_semester)
        id_list_temp_vor_sem_temp = []
        unbelegte_vorausgesetzte_kurse = []
        for i in id_list_temp_vor_sem:
            id_list_temp_vor_sem_temp.append(i[0]) #bereits belegte module (id)
        increment = 0
        kurs_voraussetzung = dbase.get_modul_voraussetzungen(str(idModule)) # Voraussetzungen für idModule
        for v in kurs_voraussetzung:
            if str(idModule) == str(v[2]) and int(v[1]) not in id_list_temp_vor_sem_temp:  # wenn idModule == modulID in voraussetzung_module
                unbelegte_vorausgesetzte_kurse.append(str(v[1])) # Vorausgesetzter kurs und noch nicht belegt
                if unbelegte_vorausgesetzte_kurse:
                    for unbelegt in unbelegte_vorausgesetzte_kurse:
                        modul_from_db = dbase.get_single_module(unbelegt)
                        #flash("Kurs hat eine Voraussetzung mit der ID " + unbelegt + " (" + modul_from_db[0][2] + "), welche du noch nicht abgeschlossen hast.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< wird als Voraussetzung für das Modul benötigt.")
                    increment = increment + 1
        if increment > 0:
            return redirect(request.url)



        elementFromDB = dbase.get_single_module(idModule)

        #Falls Wahlpflichtmodul überlassene LP übersteigt
        if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
            for i in empfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 30):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in nichtempfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 30):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in andere_empfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if(user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or(user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in andere_nichtempfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 30) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

        elif user_wahlvertiefung_ID == 2:
            for i in empfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 12):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in nichtempfohlene_wahlpflichtkurse:
                if(int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_LP_ist + temp_wahlpflicht_lp > 12):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in andere_empfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if(user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 6):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)

            for i in andere_nichtempfohlene_wahlpflichtkurse:
                if (int(idModule) == i[0]):
                    temp_wahlpflicht_lp = int(elementFromDB[0][6])
                    if (user_wahlpflicht_LP_ist + user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 12) or (user_wahlpflicht_andere_LP_ist + temp_wahlpflicht_lp > 6):
                        modul_from_db = dbase.get_single_module(idModule)
                        #flash("Wahl des Modules mit ID " + idModule + " (" + modul_from_db[0][2] + ") nicht möglich.")
                        flash("Das Modul >>" + modul_from_db[0][2] + "<< ist nicht wählbar, "
                                                                     "weil es die maximale Anzahl an Leistungspunkten im Wahlpflichtbereich überschreiten würde.")
                        return redirect(request.url)


        # Modul in benutzer_modul hinzufügen
        dbase.insert_benutzer_modul(user_id, idModule, current_semester)

        if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
            return render_template("modulauswahl.html",
                                   module1=module1,
                                   user_start_semester=user_start_semester,
                                   user_wahlvertiefung_ID=user_wahlvertiefung_ID,
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
                                   lp_gesamt=lp_gesamt,
                                   semesterwochenstunden=semesterwochenstunden,
                                   temp_list=temp_list,
                                   lp_gesamt_alle_semester = lp_gesamt_alle_semester,
                                   current_semester = current_semester,
                                   user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist_summe,
                                   semester_anzahl = semester_anzahl,
                                   andere_erlaubte_wahlpflichtkurse=andere_erlaubte_wahlpflichtkurse,
                                   andere_nichterlaubte_wahlpflichtkurse=andere_nichterlaubte_wahlpflichtkurse,
                                   andere_ausgegraute_wahlpflichtkurse=andere_ausgegraute_wahlpflichtkurse,
                                   andere_n_ausgegraute_wahlpflichtkurse=andere_n_ausgegraute_wahlpflichtkurse
                                   )
        elif user_wahlvertiefung_ID == 2:
            return render_template("modulauswahl.html",
                                   module1=module1,
                                   user_start_semester=user_start_semester,
                                   user_wahlvertiefung_ID=user_wahlvertiefung_ID,
                                   pflichtkurse_nicht_empfohlen=pflichtkurse_nicht_empfohlen,
                                   pflichtkurse_vertiefung_empfohlen=pflichtkurse_vertiefung_empfohlen,
                                   pflichtkurse_vertiefung_nicht_empfohlen=pflichtkurse_vertiefung_nicht_empfohlen,
                                   zweites_Grundlagenmodul=zweites_Grundlagenmodul,
                                   zweites_Grundlagenmodul_nicht_empfohlen=zweites_Grundlagenmodul_nicht_empfohlen,
                                   empfohlene_wahlpflichtkurse=empfohlene_wahlpflichtkurse,
                                   nichtempfohlene_wahlpflichtkurse=nichtempfohlene_wahlpflichtkurse,
                                   andere_empfohlene_wahlpflichtkurse=andere_empfohlene_wahlpflichtkurse,
                                   andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse,
                                   user_pflicht_lp_ist=user_pflicht_lp_ist,
                                   user_pflicht_lp_soll=user_pflicht_lp_soll,
                                   user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                                   user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                                   user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                                   user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                                   user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                                   user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                                   user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                                   user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                                   lp_gesamt=lp_gesamt,
                                   semesterwochenstunden=semesterwochenstunden,
                                   temp_list=temp_list,
                                   lp_gesamt_alle_semester = lp_gesamt_alle_semester,
                                   current_semester = current_semester,
                                   user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist_summe,
                                   semester_anzahl = semester_anzahl,
                                   andere_erlaubte_wahlpflichtkurse=andere_erlaubte_wahlpflichtkurse,
                                   andere_nichterlaubte_wahlpflichtkurse=andere_nichterlaubte_wahlpflichtkurse,
                                   andere_ausgegraute_wahlpflichtkurse=andere_ausgegraute_wahlpflichtkurse,
                                   andere_n_ausgegraute_wahlpflichtkurse=andere_n_ausgegraute_wahlpflichtkurse
                                   )
        elif user_wahlvertiefung_ID == 4:
            return render_template("modulauswahl.html",
                                   module1=module1,
                                   user_start_semester=user_start_semester,
                                   user_wahlvertiefung_ID = user_wahlvertiefung_ID,
                                   pflichtkurse_nicht_empfohlen=pflichtkurse_nicht_empfohlen,
                                   pflichtkurse_vertiefung_empfohlen=pflichtkurse_vertiefung_empfohlen,
                                   pflichtkurse_vertiefung_nicht_empfohlen=pflichtkurse_vertiefung_nicht_empfohlen,
                                   zweites_Grundlagenmodul=zweites_Grundlagenmodul,
                                   zweites_Grundlagenmodul_nicht_empfohlen=zweites_Grundlagenmodul_nicht_empfohlen,
                                   empfohlene_wahlpflichtkurse=empfohlene_wahlpflichtkurse,
                                   nichtempfohlene_wahlpflichtkurse=nichtempfohlene_wahlpflichtkurse,
                                   user_pflicht_lp_ist=user_pflicht_lp_ist,
                                   user_pflicht_lp_soll=user_pflicht_lp_soll,
                                   user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                                   user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                                   user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                                   user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                                   user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                                   user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                                   user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                                   user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                                   lp_gesamt=lp_gesamt,
                                   semesterwochenstunden=semesterwochenstunden,
                                   temp_list=temp_list,
                                   lp_gesamt_alle_semester=lp_gesamt_alle_semester,
                                   current_semester=current_semester,
                                   user_wahlpflicht_LP_ist_summe=user_wahlpflicht_LP_ist_summe,
                                   semester_anzahl=semester_anzahl
                                   )


    if user_wahlvertiefung_ID == 1 or user_wahlvertiefung_ID == 3:
        return render_template("modulauswahl.html",
                               module1=module1,
                               user_start_semester=user_start_semester,
                               user_wahlvertiefung_ID = user_wahlvertiefung_ID,
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
                               lp_gesamt=lp_gesamt,
                               semesterwochenstunden=semesterwochenstunden,
                               temp_list=temp_list,
                               lp_gesamt_alle_semester = lp_gesamt_alle_semester,
                               current_semester = current_semester,
                               user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist_summe,
                               semester_anzahl = semester_anzahl,
                               andere_erlaubte_wahlpflichtkurse=andere_erlaubte_wahlpflichtkurse,
                               andere_nichterlaubte_wahlpflichtkurse=andere_nichterlaubte_wahlpflichtkurse,
                               andere_ausgegraute_wahlpflichtkurse=andere_ausgegraute_wahlpflichtkurse,
                               andere_n_ausgegraute_wahlpflichtkurse=andere_n_ausgegraute_wahlpflichtkurse
                               )
    elif user_wahlvertiefung_ID == 2:
        return render_template("modulauswahl.html",
                               module1=module1,
                               user_start_semester=user_start_semester,
                               user_wahlvertiefung_ID = user_wahlvertiefung_ID,
                               pflichtkurse_nicht_empfohlen=pflichtkurse_nicht_empfohlen,
                               pflichtkurse_vertiefung_empfohlen=pflichtkurse_vertiefung_empfohlen,
                               pflichtkurse_vertiefung_nicht_empfohlen=pflichtkurse_vertiefung_nicht_empfohlen,
                               zweites_Grundlagenmodul=zweites_Grundlagenmodul,
                               zweites_Grundlagenmodul_nicht_empfohlen=zweites_Grundlagenmodul_nicht_empfohlen,
                               empfohlene_wahlpflichtkurse=empfohlene_wahlpflichtkurse,
                               nichtempfohlene_wahlpflichtkurse=nichtempfohlene_wahlpflichtkurse,
                               andere_empfohlene_wahlpflichtkurse=andere_empfohlene_wahlpflichtkurse,
                               andere_nichtempfohlene_wahlpflichtkurse=andere_nichtempfohlene_wahlpflichtkurse,
                               user_pflicht_lp_ist=user_pflicht_lp_ist,
                               user_pflicht_lp_soll=user_pflicht_lp_soll,
                               user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                               user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                               user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                               user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                               user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                               user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                               user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                               user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                               lp_gesamt = lp_gesamt,
                               semesterwochenstunden=semesterwochenstunden,
                               temp_list = temp_list,
                               lp_gesamt_alle_semester = lp_gesamt_alle_semester,
                               current_semester = current_semester,
                               user_wahlpflicht_LP_ist_summe = user_wahlpflicht_LP_ist_summe,
                               semester_anzahl = semester_anzahl,
                               andere_erlaubte_wahlpflichtkurse = andere_erlaubte_wahlpflichtkurse,
                               andere_nichterlaubte_wahlpflichtkurse = andere_nichterlaubte_wahlpflichtkurse,
                               andere_ausgegraute_wahlpflichtkurse = andere_ausgegraute_wahlpflichtkurse,
                               andere_n_ausgegraute_wahlpflichtkurse = andere_n_ausgegraute_wahlpflichtkurse
                               )
    elif user_wahlvertiefung_ID == 4:
            return render_template("modulauswahl.html",
                                   module1=module1,
                                   user_start_semester=user_start_semester,
                                   user_wahlvertiefung_ID = user_wahlvertiefung_ID,
                                   pflichtkurse_nicht_empfohlen=pflichtkurse_nicht_empfohlen,
                                   pflichtkurse_vertiefung_empfohlen=pflichtkurse_vertiefung_empfohlen,
                                   pflichtkurse_vertiefung_nicht_empfohlen=pflichtkurse_vertiefung_nicht_empfohlen,
                                   zweites_Grundlagenmodul=zweites_Grundlagenmodul,
                                   zweites_Grundlagenmodul_nicht_empfohlen=zweites_Grundlagenmodul_nicht_empfohlen,
                                   empfohlene_wahlpflichtkurse=empfohlene_wahlpflichtkurse,
                                   nichtempfohlene_wahlpflichtkurse=nichtempfohlene_wahlpflichtkurse,
                                   user_pflicht_lp_ist=user_pflicht_lp_ist,
                                   user_pflicht_lp_soll=user_pflicht_lp_soll,
                                   user_weitere_einfuehrung_LP_ist=user_weitere_einfuehrung_LP_ist,
                                   user_weitere_einfuehrung_LP_soll=user_weitere_einfuehrung_LP_soll,
                                   user_wahlpflicht_LP_ist=user_wahlpflicht_LP_ist,
                                   user_wahlpflicht_andere_LP_ist=user_wahlpflicht_andere_LP_ist,
                                   user_min_wahlpflicht_LP=user_min_wahlpflicht_LP,
                                   user_max_wahlpflicht_LP=user_max_wahlpflicht_LP,
                                   user_min_wahlpflicht_andere_LP=user_min_wahlpflicht_andere_LP,
                                   user_max_wahlpflicht_andere_LP=user_max_wahlpflicht_andere_LP,
                                   lp_gesamt=lp_gesamt,
                                   semesterwochenstunden=semesterwochenstunden,
                                   temp_list=temp_list,
                                   lp_gesamt_alle_semester=lp_gesamt_alle_semester,
                                   current_semester=current_semester,
                                   user_wahlpflicht_LP_ist_summe=user_wahlpflicht_LP_ist_summe,
                                   semester_anzahl=semester_anzahl
                                   )

@app.route('/logout')
def logout():
    logout_user()
    session.clear()
    return redirect('/')
   # return redirect(url_for('modulauswahl'))


if __name__ == '__main__':
    app.run(debug=True)
