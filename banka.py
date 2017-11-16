# Testni projekt o banki.
# Sodelavci na projektu:
# - alenFMF
# - MarinaUVP
# - PoljanecB15
# - Larisa123
# - AnjaTrop
# - SavliE12
# - kulan89
# - martincesnovar

import sqlite3

baza = "banka1.db"

class BancniTerminal:
    def __init__(self):
        self.oseba = None   # izbrana oseba
        self.racun = None   # izbran račun
        self.cur = None
        self.con = None
        self.menu = "glavniMenu"   # začetni meni
        self.zazeni()
        
    def zazeni(self):
        # Glavna zanka, ki izbira menije in izvaja ustrezne funkcije.
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
        # Meni: glavniMenu
        print("-"*10)
        print("O - Pregled Oseb")
        print("X - Izhod")
        izbira = input("> ")
        if izbira.lower() == "o":
            self.menu = "izberiOsebo"
        elif izbira.lower() == "x":
            exit()
            
    def izberiOsebo(self):
        # Meni: izberiOsebo
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
        # Meni: dodajOsebo
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
        print("R - Izpis računov")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "izberiOsebo"
            return
        elif izbira.lower() == "r":
            self.menu = "izpisRacunov"
            return
        
        
    def izpisRacunov(self):
        # Meni: izpisRačunov
        # Predpostavka: v self.oseba je izbrana oseba
        print("Izpis racunov za ", self.oseba[1:3])
        # # - izbor računa
        emso = self.oseba[0]
        self.cur.execute("SELECT Racun FROM Racun JOIN Oseba ON Racun.EMSO = Oseba.EMSO WHERE "+emso+" = Racun.EMSO") 
        print("D - Dodaj račun")
        
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
        print("I - Izpis transakcij")
        print("P - Položi")
        print("D - Dvigni")
        izbira = input("> ")
        if izbira.lower() == 'i':
            self.cur.execute("""
            SELECT RACUN, ZNESEK, DATUM FROM Transakcija
            WHERE RACUN = ?""", ('%' +  self.racun +'%',))
            transakcije = self.cur.fetchall()
            for racun, znesek, datum in transakcije:
                print(racun, znesek, datum)
        elif izbira.lower() == 'p':
            znesek = input('Vnesi znesek: ')
            #konec
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "izpisRacunov"
            return

#############
BancniTerminal()

