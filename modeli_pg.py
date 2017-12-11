import psycopg2
import csv
import auth

con = psycopg2.connect(database=auth.db, host=auth.host, user=auth.user, password=auth.password)
cur = con.cursor()

def poisciPriimek(priimek):
    cur.execute("""
        SELECT EMSO, IME, PRIIMEK, ULICA, HISNA_STEVILKA,
            Posta.POSTNA_ST, Posta.POSTA
        FROM Oseba JOIN Posta ON Oseba.POSTA = Posta.POSTNA_ST
        WHERE PRIIMEK LIKE %s
        """, ("%" + priimek + "%",))
    return cur.fetchall()

def poisciEMSO(emso):
    cur.execute("""
        SELECT EMSO, IME, PRIIMEK, ULICA, HISNA_STEVILKA,
            Posta.POSTNA_ST, Posta.POSTA
        FROM Oseba JOIN Posta ON Oseba.POSTA = Posta.POSTNA_ST
        WHERE emso = %s
        """, (emso, ))
    return cur.fetchone()

def dodajKraj(posta, kraj):
    cur.execute("""
        INSERT INTO Posta (POSTNA_ST, POSTA)
        VALUES (%s, %s)
        """, (posta, kraj))
    con.commit()

def _dodajOsebo(ime, priimek, emso, ulica, stevilka, posta):
    cur.execute("""
        INSERT INTO Oseba (IME, PRIIMEK, EMSO, ULICA,
                           HISNA_STEVILKA, POSTA)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (ime, priimek, emso, ulica, stevilka, posta))

def dodajOsebo(ime, priimek, emso, ulica, stevilka, posta):
    cur.execute("""
        SELECT * FROM Posta
        WHERE POSTNA_ST = %s
        """, (posta, ))
    if cur.fetchone() is None:
        return False
    _dodajOsebo(ime, priimek, emso, ulica, stevilka, posta)
    con.commit()
    return True

def racunEMSO(emso):
    cur.execute("""
        SELECT Racun.Racun, COALESCE(SUM(Znesek), 0), MAX(Datum) FROM Racun
        LEFT JOIN Transakcija
        ON Racun.Racun = Transakcija.Racun
        WHERE EMSO = %s
        GROUP BY Racun.Racun
        ORDER BY Racun.Racun
        """, (emso,))
    return cur.fetchall()

def emsoRacun(racun):
    cur.execute("""
        SELECT EMSO FROM Racun
        WHERE Racun = %s
    """, (racun, ))
    return cur.fetchone()

def dodajRacun(emso):
    cur.execute("""
        INSERT INTO Racun (EMSO, Racun)
        VALUES (%s, NULL)
        """, (emso,))
    con.commit()

def transakcije(racun):
    cur.execute("""
        SELECT RACUN, ZNESEK, DATUM FROM Transakcija
        WHERE RACUN = %s
        """, ('%' +  racun +'%',))
    return cur.fetchall()

def dodajTransakcijo(racun, znesek):
    cur.execute("""
        INSERT INTO Transakcija (RACUN, ZNESEK)
        VALUES (%s, %s)
    """, (racun, znesek))
    con.commit()

def uvoziPodatke(datoteka):
    with open(datoteka) as f:
        reader = csv.reader(f, delimiter = ';')
        next(reader)
        try:
            for ime, priimek, emso, ulica, stevilka, posta in reader:
                _dodajOsebo(ime, priimek, emso, ulica,
                            stevilka, posta)
        except Exception as e:
            print("Napaka: ", e)
            con.rollback()
            return False
        con.commit()
        return True
