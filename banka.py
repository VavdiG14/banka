# Testni projekt o banki.
# Sodelavci na projektu:
# - alenFMF
<<<<<<< HEAD
# - PoljanecB15
=======
# - Larisa123
>>>>>>> 8e246fced7b10a55ed3b595bdc96806faebcfd73

import sqlite3

baza = "banka1.db"

class BancniTerminal:
    def __init__(self):
        self.oseba = None
        self.racun = None
        self.cur = None
        self.con = None
        self.menu = "glavniMenu"
        self.zazeni()
        
    def zazeni(self):
        with sqlite3.connect(baza) as con:
            self.con = con
            self.cur = con.cursor()
            while True:
                if self.menu == "glavniMenu":
                    self.glavniMenu()
                elif self.menu == "izberiOsebo":
                    self.izberiOsebo()
                elif self.menu == "dodajOsebo":
                    self.dodajOsebo()
                elif self.menu == "izpisRacunov":
                    self.izpisRacunov()
                elif self.menu == "oOsebi":
                    self.oOsebi()
                elif self.menu == "oRacunu":
                    self.oRacunu()

    def glavniMenu(self):
        print("-"*10)
        print("O - Pregled Oseb")
        print("X - Izhod")
        izbira = input("> ")
        if izbira.lower() == "o":
            self.menu = "izberiOsebo"
        elif izbira.lower() == "x":
            exit()
            
    def izberiOsebo(self):
        podatki = input("Priimek osebe: ");
        self.cur.execute("""
    SELECT EMSO, IME, PRIIMEK, ULICA, HISNA_STEVILKA, Posta.POSTNA_ST, Posta.POSTA
        FROM Oseba JOIN Posta ON Oseba.POSTA = Posta.POSTNA_ST
        WHERE PRIIMEK LIKE ?""", ("%" + podatki + "%",))
        stevec = 1
        print("Izberi številko pred osebo ali drugo akcijo.")
        osebe = self.cur.fetchall()
        for emso, ime, priimek, _, _, _, _ in osebe:
            print(stevec, priimek, ime, emso)
            stevec += 1
        print("D - Dodaj osebo")
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "d":
            self.menu = "dodajOsebo"
            return
        elif izbira.lower() == "n":
            self.menu = "glavniMenu"
            return
        elif izbira.isdigit():
            n = int(izbira) - 1
            if n >= 0 and n < len(osebe):
                self.oseba = osebe[n]
                self.menu = "oOsebi"
            return
            
    def dodajOsebo(self):
        print("Dodajanje nove osebe")
        ime = input("Ime: ")
        priimek = input("Priimek: ")
        emso = input("EMŠO: ")
        ulica = input("Ulica: ")
        stevilka = input("Hišna številka: ")
        posta = input("Poštna številka: ")
        try:
            self.cur.execute("INSERT INTO Oseba (IME, PRIIMEK, EMSO, ULICA, HISNA_STEVILKA, POSTA)\
    values (?,?,?,?,?,?)", (ime, priimek, emso, ulica, stevilka, posta))
            self.con.commit()
            print("Vnos osebe", ime, priimek, "uspešen")     
        except Exception as e:
            print("Neuspešen vnos. Poskusi ponovno.", e)
        self.menu = "glavniMenu"

    def oOsebi(self):
        # Meni: "oOsebi"
        # Predpostavka: v self.oseba je izbrana oseba
        emso, ime, priimek, ulica, hisna_stevilka, posta, kraj = self.oseba
        print("""{0} {1}
EMŠO: {2}
Naslov: {3} {4}, {5} {6}""".format(ime, priimek, emso, ulica, hisna_stevilka, posta, kraj))
        # P - Popravi podatke (naredimo kasneje)
        # R - Izpis računov       
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "izberiOsebo"
            return
        
        
    def izpisRacunov(self):
        # Meni: izpisRačunov
        # Predpostavka: v self.oseba je izbrana oseba
        print("Izpis racunov za ", self.oseba)
        # # - izbor računa
        # D - Dodaj račun (ne gremo v nov meni, samo dodamo)
        # N - Nazaj
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "oOsebi"
            return

    def oRacunu(self):
        # Meni: oRacunu
        # Predpostavke: v self.oseba je izbrana oseba
        # v self.racun je izbran racun
        # Izpis stanja.
        # I - Izpis transakcij
        # P - Položi
        # D - Dvigni
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "izpisRacunov"
            return

#############
BancniTerminal()

