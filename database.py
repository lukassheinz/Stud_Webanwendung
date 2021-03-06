from sqlalchemy import create_engine


# Datenbank anbinden
class Database:
    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)

    def get_vertiefungen(self):
        return self.engine.execute('select * from vertiefung').fetchall()

    def get_vertiefungen2(self, vertiefung_ID):
        return self.engine.execute("select * from vertiefung where ID =" + str(vertiefung_ID)).fetchall()

    def get_single_module(self, modul_ID):
        sql_query = "select * from modul where ID = %s"
        parameter = (str(modul_ID))
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_user(self, matrikelnummer, passwort_hash):
        sql_query = "select * from benutzer where matrikelnummer = %s and passwort = %s"
        parameter = (matrikelnummer, passwort_hash)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_empfohlen(self, start_semester, current_semester):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = "select * from modul where empfohlen_ab <= %s and angebotshaeufigkeit LIKE %s"
        parameter = (str(current_semester), sem)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_nicht_empfohlen(self, start_semester, current_semester):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = "select * from modul where empfohlen_ab > %s and angebotshaeufigkeit LIKE %s"
        parameter = (str(current_semester), sem)
        return self.engine.execute(sql_query, parameter).fetchall()

    #
    def get_modul(self):
        return self.engine.execute('select * from modul').fetchall()

    # NEW * NEW * NEW * NEW * NEW

    def get_modul_mit_voraussetzung(self):
        sql_query = """
            SELECT DISTINCT m1.*, 
                            m2.ID v_ID, 
                            m2.nummer v_nummer, 
                            m2.modultitel v_modultitel, 
                            m2.pflicht_wahlpflicht v_pflicht_wahlpflicht, 
                            m2.empfohlen_ab v_empfohlen_ab, 
                            m2.angebotshaeufigkeit v_angebotshaeufigkeit, 
                            m2.leistungspunkte v_leistungspunkte, 
                            m2.semesterwochenstunden v_semesterwochenstunden, 
                            m2.voraussetzungslp v_vorausssetzungslp 
            FROM modul m1 
            LEFT JOIN voraussetzung_modul ON voraussetzung_modul.modul_ID = m1.ID 
            LEFT JOIN modul m2 ON m2.ID = voraussetzung_modul.modulvoraussetzung_ID
            """

    # Eingabe eines Benutzers
    def insert_benutzer(self, vorname, nachname, email, passwort):
        sql_query = """
            INSERT INTO benutzer(vorname, nachname, email, passwort) 
            VALUES(%s,%s,%s,%s)
            """
        parameter = (vorname, nachname, email, passwort)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Eingabe eines Studenten
    def insert_student(self, vorname, nachname, email, passwort, immatrikulationssemester, immatrikulationsjahr):
        sql_query = """
            INSERT INTO benutzer(vorname, 
                                 nachname, 
                                 email, 
                                 passwort, 
                                 immatrikulationssemester, 
                                 immatrikulationsjahr) 
            VALUES(%s,%s,%s,%s,%s,%s)
            """
        parameter = (vorname, nachname, email, passwort, immatrikulationssemester, immatrikulationsjahr)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Aktualisierung eines Benutzers
    def update_benutzer(self, id, vorname, nachname, email, passwort, wahlvertiefung_id, immatrikulationssemester,
                        immatrikulationsjahr):
        sql_query = """
            UPDATE benutzer 
            SET vorname = %s, 
                nachname = %s, 
                email = %s, 
                passwort = %s, 
                wahlvertiefung_ID = %s, 
                immatrikulationssemester = %s, 
                immatrikulationsjahr = %s 
            WHERE id = %s
            """
        parameter = (vorname,
                     nachname,
                     email,
                     passwort,
                     wahlvertiefung_id,
                     immatrikulationssemester,
                     immatrikulationsjahr,
                     id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # L??schen eines Benutzers
    def delete_benutzer(self, id):
        sql_query = """
            DELETE FROM benutzer 
            WHERE id = %s"""
        parameter = (id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Abfrage eines Benutzers
    def get_benutzer(self, id):
        sql_query = """
            SELECT *
            FROM benutzer
            WHERE id = %s
        """
        parameter = (id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Eingabe eines Moduls
    def insert_modul(self,
                     nummer,
                     modultitel,
                     pflicht_wahlpflicht,
                     empfohlen_ab,
                     angebotshaeufigkeit,
                     leistungspunkte,
                     semesterwochenstunden,
                     voraussetzungslp):
        sql_query = """
            INSERT INTO modul(nummer, 
                              modultitel, 
                              pflicht_wahlpflicht, 
                              empfohlen_ab, 
                              angebotshaeufigkeit, 
                              leistungspunkte, 
                              semesterwochenstunden, 
                              voraussetzungslp) 
            VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
            """
        parameter = (nummer,
                     modultitel,
                     pflicht_wahlpflicht,
                     empfohlen_ab,
                     angebotshaeufigkeit,
                     leistungspunkte,
                     semesterwochenstunden,
                     voraussetzungslp)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Aktualisierung eines Moduls
    def update_modul(self, id, nummer, modultitel, pflicht_wahlpflicht, empfohlen_ab, angebotshaeufigkeit,
                     leistungspunkte, semesterwochenstunden, voraussetzungslp):
        sql_query = """
            UPDATE modul 
            SET nummer = %s, 
                modultitel = %s, 
                pflicht_wahlpflicht = %s, 
                empfohlen_ab = %s, 
                angebotshaeufigkeit = %s, 
                leistungspunkte = %s, 
                semesterwochenstunden = %s, 
                voraussetzungslp = %s 
            WHERE id = %s
            """
        parameter = (nummer, modultitel, pflicht_wahlpflicht, empfohlen_ab, angebotshaeufigkeit, leistungspunkte,
                     semesterwochenstunden, voraussetzungslp, id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # L??schen eines Moduls
    def delete_modul(self, id):
        sql_query = """
            DELETE FROM modul
            WHERE id = %s
            """
        parameter = (id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Eingabe des Status 'belegt' f??r ein Modul eines Benutzers
    def insert_benutzer_modul(self, benutzer_id, modul_id, semester):
        sql_query = """
            INSERT INTO benutzer_modul(benutzer_id, modul_id, semester, status) 
            VALUES(%s,%s,%s,'belegt')
            """
        parameter = (benutzer_id, modul_id, semester)
        return self.engine.execute(sql_query, parameter)

    # ??nderung des Status auf 'abgeschlossen' f??r ein Modul eines Benutzers
    def update_benutzer_modul(self, benutzer_id, modul_id, semester):
        sql_query = """
            UPDATE benutzer_modul 
            SET semester = %s, status = 'abgeschlossen' 
            WHERE benutzer_id = %s and modul_id = %s
            """
        parameter = (semester,benutzer_id, modul_id)
        return self.engine.execute(sql_query, parameter)

    # ??nderung des Status auf 'belegt' f??r ein Modul eines Benutzers
    def update_benutzer_modul_belegt(self, benutzer_id, modul_id, semester):
        sql_query = """
            UPDATE benutzer_modul 
            SET semester = %s, status = 'belegt' 
            WHERE benutzer_id = %s and modul_id = %s
            """
        parameter = (semester, benutzer_id, modul_id)
        return self.engine.execute(sql_query, parameter)

    # Zuordnung eines Moduls zu einer Vertiefung
    def insert_vertiefung_modul(self, vertiefung_id, modul_id, zuordnung):
        sql_query = """
            INSERT INTO vertiefung_modul(vertiefung_id, modul_id, zuordnung) 
            VALUES(%s,%s,%s)
            """
        parameter = (vertiefung_id, modul_id, zuordnung)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Eingabe einer Modulvoraussetzung f??r ein Modul
    def insert_voraussetzung_modul(self, modulvoraussetzung_id, modul_id):
        sql_query = """
            INSERT INTO voraussetzung_modul(modulvoraussetzung_id, modul_id) 
            VALUES(%s,%s)
            """
        parameter = (modulvoraussetzung_id, modul_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # ??nderung der Modulvoraussetzung eines Moduls
    def update_voraussetzung_modul(self, old_modulvoraussetzung_id, modul_id, new_modulvoraussetzung_id):
        sql_query = """
            UPDATE voraussetzung_modul 
            SET modulvoraussetzung_id = %s
            WHERE modul_id = %s AND modulvoraussetzung_id = %s
            """
        parameter = (new_modulvoraussetzung_id, modul_id, old_modulvoraussetzung_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # L??schen einer Modulvoraussetzung eines Moduls
    def delete_voraussetzung_modul(self, modulvoraussetzung_id, modul_id):
        sql_query = """
            DELETE FROM voraussetzung_modul 
            WHERE modulvoraussetzung_id = %s AND modul_id = %s
            """
        parameter = (modulvoraussetzung_id, modul_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Alle Module die im Sommersemester und in beiden Semestern  belegt werden k??nnen ausgeben
    def get_ModuleSOSE(self):
        return self.engine.execute('SELECT * FROM Modul WHERE angebotshaeufigkeit like "%so%"').fetchall()

    # Alle Module die im Wintersemester und in beiden Semestern belegt werden k??nnen ausgeben
    def get_ModuleWISE(self):
        return self.engine.execute('SELECT * FROM Modul WHERE angebotshaeufigkeit like "%wi%"').fetchall()

    ###################################################################
    # Alle Module mit ihren Voraussetzungsmodulen (ausf??hrliche Version)
    def get_Voraussetzungsmodule1(self):
        return self.engine.execute(
            'SELECT m.ID AS ID, m.nummer AS nummer, m.modultitel AS modultitel,m.empfohlen_ab as empfohlen_ab, m.angebotshaeufigkeit as angebotshaeufigkeit, m.leistungspunkte as leistungspunkte, m.semesterwochenstunden as semesterwochenstunden, m.voraussetzungslp as voraussetzungslp, v.modulvoraussetzung_id as modulvoraussetzung, x.nummer as nummer, x.modultitel as Modultitel_Voraussetzungsmodul FROM Modul m Join Voraussetzung_Modul v on m.id = v.modul_id Join Modul x on v.modulvoraussetzung_id = x.id').fetchall()

    # Alle Module mit ihren Voraussetzungsmodulen (kurze Version)
    def get_Voraussetzungsmodule2(self):
        return self.engine.execute(
            'SELECT m.ID AS ID, m.nummer AS nummer, m.modultitel AS modultitel, v.modulvoraussetzung_id as modulvoraussetzung, x.nummer as nummer, x.modultitel as Modultitel_Voraussetzungsmodul FROM Modul m Join Voraussetzung_Modul v on m.id = v.modul_id Join Modul x on v.modulvoraussetzung_id = x.id').fetchall()

    ### LEISTUNGSPUNKTE ###

    # LP-Summe der Grund_Pflichtmodule ohne Vertiefung
    def get_Gesamtsumme_LP(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        WHERE benutzer_ID = %s;
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Grund_Pflichtmodule ohne Vertiefung
    def get_Summe_Pflichtmodule(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        WHERE benutzer_ID = %s AND m.pflicht_wahlpflicht = "Pflicht";
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Pflichtmodule eines Benutzers mit gew??hlter Vertiefung
    def get_Summe_Pflicht_Vertiefung(self, id, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        WHERE (m.pflicht_wahlpflicht = "Pflicht" OR m.ID IN (
            SELECT modul_ID
		    FROM vertiefung_modul vm
		    JOIN benutzer b ON b.wahlvertiefung_ID = vm.vertiefung_ID
		    WHERE b.ID = %s AND zuordnung = "Pflicht_in")) 
        AND m.ID IN (
                SELECT modul_ID
		        FROM benutzer_modul
                WHERE benutzer_ID = %s AND semester = %s)
        """
        parameter = (id, benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Pflichtmodule eines Benutzers mit gew??hlter Vertiefung Vor
    def get_Summe_Pflicht_Vertiefung_Vor(self, id, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        WHERE (m.pflicht_wahlpflicht = "Pflicht" OR m.ID IN (
            SELECT modul_ID
    	    FROM vertiefung_modul vm
    	    JOIN benutzer b ON b.wahlvertiefung_ID = vm.vertiefung_ID
		    WHERE b.ID = %s AND zuordnung = "Pflicht_in")) 
        AND m.ID IN (
                SELECT modul_ID
		        FROM benutzer_modul                    
		        WHERE benutzer_ID = %s AND semester < %s)
        """
        parameter = (id, benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Pflichtmodule eines Benutzers mit gew??hlter Vertiefung Gesamt
    def get_Summe_Pflicht_Vertiefung_Gesamt(self, id, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        WHERE (m.pflicht_wahlpflicht = "Pflicht" OR m.ID IN (
            SELECT modul_ID
		    FROM vertiefung_modul vm
    		JOIN benutzer b ON b.wahlvertiefung_ID = vm.vertiefung_ID
    	    WHERE b.ID = %s AND zuordnung = "Pflicht_in")) 
        AND m.ID IN (
                SELECT modul_ID
    		    FROM benutzer_modul
                WHERE benutzer_ID = %s)
        """
        parameter = (id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule in der gew??hlten Vertiefung eines Benutzers
    def get_Summe_WPF_Vertiefung(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung = "gehoert_zu" AND bm.semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule in der gew??hlten Vertiefung eines Benutzers Vorherige Semester
    def get_Summe_WPF_Vertiefung_Vor(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung = "gehoert_zu" AND bm.semester < %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule in der gew??hlten Vertiefung eines Benutzers Gesamt
    def get_Summe_WPF_Vertiefung_Gesamt(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung = "gehoert_zu";
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule der anderen Vertiefungen eines Benutzers
    def get_Summe_WPF_andere(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung IN ("empfohlen_in", "erlaubt_in", "nicht_empfohlen_in") AND semester= %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule der anderen Vertiefungen eines Benutzers Vorherige Semester
    def get_Summe_WPF_andere_Vor(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung = "erlaubt_in" AND semester < %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Wahlpflichtmodule der anderen Vertiefungen eines Benutzers Gesamt
    def get_Summe_WPF_andere_Gesamt(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung IN ("empfohlen_in", "erlaubt_in", "nicht_empfohlen_in");
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Grundlagenpraktika eines Benutzers
    def get_Summe_Grundlagenpraktika(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Grundlagenpraktikum" AND vm.zuordnung = "erlaubt_in" AND semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Grundlagenpraktika eines Benutzers vorherige Semester
    def get_Summe_Grundlagenpraktika_Vor(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Grundlagenpraktikum" AND vm.zuordnung = "erlaubt_in" AND semester < %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe der Grundlagenpraktika eines Benutzers
    def get_Summe_Grundlagenpraktika_Gesamt(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Grundlagenpraktikum" AND vm.zuordnung = "erlaubt_in";
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe weitere Einfuehrungsmodule eines Benutzers
    def get_Summe_weitere_Einfuehrung(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "erlaubt_in" AND semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe weitere Einfuehrungsmodule eines Benutzers Vorherige Semester
    def get_Summe_weitere_Einfuehrung_Vor(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "erlaubt_in" AND semester < %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # LP-Summe weitere Einfuehrungsmodule eines Benutzers Gesamt
    def get_Summe_weitere_Einfuehrung_Gesamt(self, benutzer_id):
        sql_query = """
        SELECT IFNULL(SUM(leistungspunkte), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "erlaubt_in";
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    ### SEMESTERWOCHENSTUNDEN ###

    # SWS-Summe der Pflichtmodule eines Benutzers mit gew??hlter Vertiefung
    def get_Summe_Pflicht_Vertiefung_sws(self, id, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(semesterwochenstunden), 0)
        FROM modul m
        WHERE (m.pflicht_wahlpflicht = "Pflicht" OR m.ID IN (
            SELECT modul_ID
		    FROM vertiefung_modul vm
    	    JOIN benutzer b ON b.wahlvertiefung_ID = vm.vertiefung_ID
    	    WHERE b.ID = %s AND zuordnung = "Pflicht_in")) 
        AND m.ID IN (
                SELECT modul_ID
		        FROM benutzer_modul
                WHERE benutzer_ID = %s AND semester = %s)
        """
        parameter = (id, benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

        # SWS-Summe der Wahlpflichtmodule in der gew??hlten Vertiefung eines Benutzers

    def get_Summe_WPF_Vertiefung_sws(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(semesterwochenstunden), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung = "gehoert_zu" AND bm.semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

        # SWS-Summe der Wahlpflichtmodule der anderen Vertiefungen eines Benutzers

    def get_Summe_WPF_andere_sws(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(semesterwochenstunden), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Wahlpflicht" AND vm.zuordnung IN ("empfohlen_in", "erlaubt_in", "nicht_empfohlen_in") AND semester= %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # SWS-Summe der Grundlagenpraktika eines Benutzers
    def get_Summe_Grundlagenpraktika_sws(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(semesterwochenstunden), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Grundlagenpraktikum" AND vm.zuordnung = "erlaubt_in" AND semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # SWS-Summe weitere Einfuehrungsmodule eines Benutzers
    def get_Summe_weitere_Einfuehrung_sws(self, benutzer_id, semester):
        sql_query = """
        SELECT IFNULL(SUM(semesterwochenstunden), 0)
        FROM modul m
        JOIN benutzer_modul bm ON bm.modul_ID = m.ID
        JOIN benutzer b ON b.ID = bm.benutzer_ID
        JOIN vertiefung_modul vm ON vm.vertiefung_ID = b.wahlvertiefung_ID AND vm.modul_ID = m.ID 
        AND benutzer_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "erlaubt_in" AND semester = %s;
        """
        parameter = (benutzer_id, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Anzeige der Modulvoraussetzungen aller nicht belegten Module eines Benutzers
    def get_Voraussetzung_nicht_belegter_Module(self, benutzer_id):
        sql_query = """
        SELECT DISTINCT m. *
        FROM modul m
        JOIN voraussetzung_modul vm ON vm.modulvoraussetzung_ID = m.ID
        WHERE m.ID
        NOT IN(SELECT modul_ID FROM benutzer_modul WHERE benutzer_ID = %s);
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_empfohlen_pflicht(self, start_semester, current_semester, p_w, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """
        select *
        from modul m 
        where empfohlen_ab <= %s 
        and angebotshaeufigkeit LIKE %s 
        and pflicht_wahlpflicht = %s
        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                    """
        parameter = (str(current_semester), sem, p_w, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_empfohlen_wahlpflicht(self, start_semester, current_semester, p_w, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = "select * from modul m where empfohlen_ab <= %s and angebotshaeufigkeit LIKE %s and pflicht_wahlpflicht = %s and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)"
        parameter = (str(current_semester), sem, p_w, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_nicht_empfohlen_pflicht(self, start_semester, current_semester, p_w, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = "select * from modul m where empfohlen_ab > %s and angebotshaeufigkeit LIKE %s and pflicht_wahlpflicht = %s and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)"
        parameter = (str(current_semester), sem, p_w, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_module_nicht_empfohlen_wahlpflicht(self, start_semester, current_semester, p_w, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = "select * from modul m where empfohlen_ab > %s and angebotshaeufigkeit LIKE %s and pflicht_wahlpflicht = %s and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)"
        parameter = (str(current_semester), sem, p_w, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    #### die n??tigen Pflichtlp f??r die Pflichtmodule / Wahlpflichtmodule f??r die jeweilige Vertiefung ####

    # Pflichtmodule
    def get_Summe_Pflichtmodule_Vertiefung(self, vertiefung_id):
        return self.engine.execute(
            'SELECT SUM(leistungspunkte) FROM modul m LEFT JOIN vertiefung_modul vm ON vm.modul_ID = m.ID WHERE pflicht_wahlpflicht = "Pflicht" OR (vertiefung_ID = ' + str(
                vertiefung_id) + ' AND pflicht_wahlpflicht = "Wahlpflicht" AND zuordnung = "Pflicht_in");').fetchall()

    #######
    def get_modul_voraussetzungen(self, modul_id):
        return self.engine.execute("select * from voraussetzung_modul where modul_ID = " + modul_id).fetchall()

    def get_modul_voraussetzungen_nach(self, modul_id):
        return self.engine.execute(
            "select * from voraussetzung_modul where modulvoraussetzung_ID = " + modul_id).fetchall()

    ### die vertiefungs-id angibt das Grundlagenmodul zur vertiefung
    def get_Einfuehrung_zu_Vertiefung(self, vertiefung_id):
        return self.engine.execute(
            'SELECT * FROM modul m JOIN vertiefung_modul vm ON vm.modul_ID = m.ID WHERE vertiefung_ID = ' + str(
                vertiefung_id) + ' AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "Pflicht_in";').fetchall()

    #################################################################
    # Alle Module aus Vertiefung x
    def get_VertiefungModule(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = 'gehoert_zu' 
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab <= %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

        # Alle Module aus Vertiefung x (nicht empfohlene Module)

    def get_nichtEmpfohleneVertiefungModule(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = 'gehoert_zu' 
                        JOIN Vertiefung x on v.vertiefung_id = x.id WHERE m.empfohlen_ab > %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

        # Module aus anderen Vertiefungen f??r Vertiefung x

    def get_andereModule(self, start_semester, current_semester, zuordnung, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = %s 
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab <= %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s AND m.pflicht_wahlpflicht = 'Wahlpflicht'
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (zuordnung, str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Module aus anderen Vertiefungen f??r Vertiefung x (nicht Empfohlene Module)
    def get_nichtEmpfohleneAndereModule(self, start_semester, current_semester, zuordnung, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = %s 
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab > %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s AND m.pflicht_wahlpflicht = 'Wahlpflicht'
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (zuordnung, str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

        # Pflicht Module der jewiligen Vertiefung

    def get_VertiefungPflichtModule(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID,
                        m.nummer AS nummer,
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht,
                        m.empfohlen_ab as empfohlen_ab,
                        m.angebotshaeufigkeit as angebotshaeufigkeit,
                        m.leistungspunkte as leistungspunkte,
                        m.semesterwochenstunden as semesterwochenstunden,
                        m.voraussetzungslp as voraussetzungslp,
                        v.vertiefung_id as vertiefung_id,
                        x.name as name
                        from Modul m
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = 'pflicht_in'
                        JOIN Vertiefung x on v.vertiefung_id = x.id
                        WHERE m.empfohlen_ab <= %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Pflicht Module der jeweilige Vertiefung (nicht empfohlene)
    def get_nichtEmpfohleneVertiefungPflichtModule(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  AND v.zuordnung = 'pflicht_in' 
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab > %s AND m.angebotshaeufigkeit LIKE %s AND v.vertiefung_id = %s
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    ################################################################################
    def get_Einfuehrung_zu_Vertiefung2(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """
                        SELECT *
                        FROM modul m
                        JOIN vertiefung_modul vm ON vm.modul_ID = m.ID
                        WHERE empfohlen_ab <= %s AND angebotshaeufigkeit LIKE %s AND vertiefung_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "Pflicht_in";
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                            """
        parameter = (str(current_semester), sem, str(vertiefung_id), benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_Einfuehrung_zu_Vertiefung3(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """
                        SELECT *
                        FROM modul m
                        JOIN vertiefung_modul vm ON vm.modul_ID = m.ID
                        WHERE empfohlen_ab > %s AND angebotshaeufigkeit LIKE %s AND vertiefung_ID = %s AND m.pflicht_wahlpflicht = "Einfuehrung" AND vm.zuordnung = "Pflicht_in";
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                            """
        parameter = (str(current_semester), sem, str(vertiefung_id), benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    ####NEW###
    # Ausgabe Grundlagenpraktikum der jewiligen Vertiefung
    def get_Grundlagenpraktikum_zu_Vertiefung(self, start_semester, current_semester, vertiefung_id, benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab <= %s AND m.angebotshaeufigkeit LIKE %s 
                        AND v.vertiefung_id = %s AND m.pflicht_wahlpflicht = 'Grundlagenpraktikum'
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s)
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    # Ausgabe Grundlagenpraktikum der jeweiligen Vertiefung (in nicht empfohlenen Semester)
    def get_Grundlagenpraktikum_zu_Vertiefung_nicht_empfohlen(self, start_semester, current_semester, vertiefung_id,
                                                              benutzer_id):
        if start_semester == 1:
            sem = '%So%' if current_semester % 2 == 0 else '%Wi%'
        else:
            sem = '%Wi%' if current_semester % 2 == 0 else '%So%'
        sql_query = """SELECT m.ID AS ID, 
                        m.nummer AS nummer, 
                        m.modultitel AS modultitel,
                        m.pflicht_wahlpflicht as pflicht_wahlpflicht, 
                        m.empfohlen_ab as empfohlen_ab, 
                        m.angebotshaeufigkeit as angebotshaeufigkeit, 
                        m.leistungspunkte as leistungspunkte, 
                        m.semesterwochenstunden as semesterwochenstunden, 
                        m.voraussetzungslp as voraussetzungslp, 
                        v.vertiefung_id as vertiefung_id, 
                        x.name as name 
                        from Modul m 
                        join vertiefung_modul v ON m.id = v.modul_id  
                        JOIN Vertiefung x on v.vertiefung_id = x.id 
                        WHERE m.empfohlen_ab > %s AND m.angebotshaeufigkeit LIKE %s 
                        AND v.vertiefung_id = %s AND m.pflicht_wahlpflicht = 'Grundlagenpraktikum'
                        and not exists (SELECT 1 FROM benutzer_modul WHERE modul_ID = m.id AND benutzer_ID = %s) 
                        """
        parameter = (str(current_semester), sem, vertiefung_id, benutzer_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_gewaehlte_module(self, benutzer_ID, semester):
        sql_query = "SELECT * FROM benutzer_modul WHERE benutzer_ID = %s and semester = %s"
        parameter = (str(benutzer_ID), semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_alle_gewaehlte_module(self, benutzer_ID):
        return self.engine.execute("SELECT modul_ID FROM benutzer_modul WHERE benutzer_ID = " + str(benutzer_ID)).fetchall()

    def get_gewaehltes_modul(self, benutzer_ID, modul_id):
        sql_query = "SELECT * FROM benutzer_modul WHERE benutzer_ID = %s and modul_ID = %s"
        parameter = (str(benutzer_ID), modul_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def delete_belegtes_modul(self, ID):
        return self.engine.execute("DELETE FROM benutzer_modul WHERE ID = " + str(ID))

    def get_vorherige_belegte_modul_ids(self, benutzer_id, current_semester):
        sql_query = "select modul_ID from benutzer_modul where benutzer_ID = %s and semester < %s"
        parameter = (benutzer_id, current_semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_nachfolgende_belegte_modul_ids(self, benutzer_id, current_semester):
        sql_query = "select modul_ID from benutzer_modul where benutzer_ID = %s and semester > %s"
        parameter = (benutzer_id, current_semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    def update_current_semester(self, user_id, new_current_semester):
        sql_query = """
                    update benutzer
                    set current_semester = %s where ID = %s
                    """
        parameter = (new_current_semester, user_id)
        return self.engine.execute(sql_query, parameter)

    def update_semester_anzahl(self, user_id, semester_anzahl):
        sql_query = """
                    update benutzer
                    set semester_anzahl = %s where ID = %s
                    """
        parameter = (semester_anzahl, user_id)
        return self.engine.execute(sql_query, parameter)

    def delete_gew??hlte_module_in_semester(self, user_id, semester_anzahl):
        sql_query = """
                    delete from benutzer_modul
                    where benutzer_ID = %s and semester = %s
                    """
        parameter = (user_id, semester_anzahl)
        return self.engine.execute(sql_query, parameter)

    def get_ausgew??hlte_module_infos(self, benutzer_ID, semester):
        sql_query = """
                    SELECT *
                    FROM modul m
                    JOIN benutzer_modul bm ON bm.modul_ID = m.ID
                    WHERE benutzer_ID = %s AND semester = %s
                    """
        parameter = (benutzer_ID, semester)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_modul_from_benutzer_modul(self, user_id, modul_id):
        sql_query = """
                    SELECT * FROM benutzer_modul WHERE benutzer_ID = %s and modul_ID = %s
                    """
        parameter = (user_id, modul_id)
        return self.engine.execute(sql_query, parameter).fetchall()

    def get_semester_of_module(self, user_id, modul_id):
        sql_query = """
                    SELECT semester
                    FROM benutzer_modul
                    where benutzer_ID = %s and modul_ID = %s"""
        parameter = (user_id, modul_id)
        return self.engine.execute(sql_query, parameter).fetchall()

 # SWAP-MODULE

    def swap_module(self, benutzer_id, modul1_id, modul2_id):
        sql_query_select = """
        SELECT semester
        FROM benutzer_modul
        WHERE benutzer_ID = %s AND modul_ID = %s
        """

        sql_query_update = """
        UPDATE benutzer_modul
        SET semester = %s
        WHERE benutzer_ID = %s AND modul_ID = %s
        """

        parameter = (benutzer_id, modul1_id)
        ergebnis_1 = self.engine.execute(sql_query_select, parameter).fetchall()
        semester_1 = ergebnis_1[0][0]

        parameter = (benutzer_id, modul2_id)
        ergebnis_2 = self.engine.execute(sql_query_select, parameter).fetchall()
        semester_2 = ergebnis_2[0][0]

        parameter = (semester_2, benutzer_id, modul1_id)
        self.engine.execute(sql_query_update, parameter).fetchall()

        parameter = (semester_1, benutzer_id, modul2_id)
        self.engine.execute(sql_query_update, parameter).fetchall()


    def update_semester(self, semester, benutzer_id, modul_id):
        sql_query = """
        UPDATE benutzer_modul
        SET semester = %s
        WHERE benutzer_ID = %s AND modul_ID = %s
        """
        parameter = (semester, benutzer_id, modul_id)
        return self.engine.execute(sql_query, parameter)


# L??schen der Module nach ??nderung der Vertiefung

    def delete_module_von_benutzer(self, benutzer_id):
        sql_query = """
        DELETE FROM benutzer_modul
        WHERE benutzer_ID = %s
        """
        parameter = (benutzer_id)
        return self.engine.execute(sql_query, parameter)
