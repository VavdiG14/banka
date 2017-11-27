import sqlite3

baza = "banka1.db"
con = sqlite3.connect(baza)
cur = con.cursor()

def poisciPriimek(priimek):
    cur.execute("""
        SELECT EMSO, IME, PRIIMEK, ULICA, HISNA_STEVILKA,
            Posta.POSTNA_ST, Posta.POSTA
        FROM Oseba JOIN Posta ON Oseba.POSTA = Posta.POSTNA_ST
        WHERE PRIIMEK LIKE ?
        """, ("%" + priimek + "%",))
    return cur.fetchall()
    
def dodajKraj(posta, kraj):
    cur.execute("""
        INSERT INTO Posta (POSTNA_ST, POSTA)
        VALUES (?, ?)
        """, (posta, kraj))
    con.commit()

def dodajOsebo(ime, priimek, emso, ulica, stevilka, posta):
    cur.execute("""
        SELECT * FROM Posta
        WHERE POSTNA_ST = ?
        """, (posta, ))
    if cur.fetchone() is None:
        return False
    cur.execute("""
        INSERT INTO Oseba (IME, PRIIMEK, EMSO, ULICA,
                           HISNA_STEVILKA, POSTA)
        VALUES (?,?,?,?,?,?)
        """, (ime, priimek, emso, ulica, stevilka, posta))
    con.commit()
    return True

def racunEMSO(emso):
    cur.execute("""
        SELECT Racun FROM Racun JOIN Oseba
            ON Racun.EMSO = Oseba.EMSO
        WHERE Oseba.EMSO = ?
        """, (emso,))
    return cur.fetchall()

def dodajRacun(emso):
    cur.execute("""
        INSERT INTO Racun (EMSO, Racun)
        VALUES (?, NULL)
        """, (emso,))
    con.commit()

def transakcije(racun):
    self.cur.execute("""
        SELECT RACUN, ZNESEK, DATUM FROM Transakcija
        WHERE RACUN = ?
        """, ('%' +  racun +'%',))
    return cur.fetchall()
