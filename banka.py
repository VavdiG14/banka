# Testni projekt o banki.
import sqlite3

baza = "banka1.db"

class BancniTerminal:
    def __init__(self):
        self.oseba = None
        self.racun = None
        self.cur = None
        self.con = None
        self.menu = "glavni"
        self.zazeni()
        
    def zazeni(self):
        with sqlite3.connect(baza) as con:
            self.con = con
            self.cur = con.cursor()
            while True:
                if self.menu == "glavni":
                    self.glavniMenu()
                elif self.menu == "oseba":
                    self.izberiOsebo()
                elif self.menu == "dodajOsebo":
                    self.dodajOsebo()
                elif self.menu == "izpisRacunov":
                    self.izpisRacunov()
                elif self.menu == "oOsebi":
                    self.oOsebi()

    def glavniMenu(self):
        print("-"*10)
        print("O - Pregled Oseb")
        print("X - Izhod")
        izbira = input("> ")
        if izbira.lower() == "o":
            self.menu = "oseba"
        elif izbira.lower() == "x":
            exit()
            
    def izberiOsebo(self):
        podatki = input("Priimek osebe: ");
        self.cur.execute("SELECT EMSO, IME, PRIIMEK FROM Oseba WHERE PRIIMEK LIKE ?", ("%" + podatki + "%",))
        stevec = 1
        print("Izberi številko pred osebo ali drugo akcijo.")
        osebe = self.cur.fetchall()
        for emso, ime, priimek in osebe:
            print(stevec, priimek, ime, emso)
            stevec += 1
        print("D - Dodaj osebo")
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "d":
            self.menu = "dodajOsebo"
            return
        elif izbira.lower() == "n":
            self.menu = "glavni"
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
        except Exception as e:
            print("Neuspešen vnos. Poskusi ponovno.", e)
        print("Vnos osebe", ime, priimek, "uspešen")     
        self.menu = "glavni"

    def oOsebi(self):
        print("Podatki o osebi")
        
    def izpisRacunov(self):
        print("Izpis racunov za ", self.oseba)
        self.menu = "glavni"
        
BancniTerminal()

