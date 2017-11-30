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

import modeli

class BancniTerminal:
    def __init__(self):
        self.oseba = None   # izbrana oseba
        self.racun = None   # izbran račun
        self.menu = "glavniMenu"   # začetni meni
        self.zazeni()
        
    def zazeni(self):
        # Glavna zanka, ki izbira menije in izvaja ustrezne funkcije.
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
        stevec = 1
        print("Izberi številko pred osebo ali drugo akcijo.")
        osebe = modeli.poisciPriimek(podatki)
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
            if not modeli.dodajOsebo(ime, priimek, emso, ulica,
                                     stevilka, posta):
                kraj = input("Kraj: ")
                modeli.dodajKraj(posta, kraj)
                modeli.dodajOsebo(ime, priimek, emso, ulica,
                                  stevilka, posta)
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
        print("Izpis računov za:", self.oseba[1] + " " + self.oseba[2])
        # # - izbor računa
        emso = self.oseba[0]
        racuni = racunEMSO(emso)
        stevec = 1
        for racun in racuni:
            print(stevec, racun)
            stevec += 1
            
        # D - Dodaj račun (ne gremo v nov meni, samo dodamo)
        # N - Nazaj
        print("D - Dodaj račun")
        print("N - Nazaj")
        izbira = input("> ")
        if izbira.lower() == "n":
            self.menu = "oOsebi"
            return
        elif izbira.lower() == "d":
            print("Ali ste prepričani, da bi radi dodali račun za osebo:", self.oseba[1] + " " + self.oseba[2])
            # Y - Da, dodaj nov račun
            # N - Nazaj
            izbira = input(">")
            if izbira.lower() == "y":
                try:
                    modeli.dodajRacun(emso)
                    print("Vnos novega računa uspešen")
                except Exception as e:
                    print("Neuspešen vnos. Poskusi ponovno.", e)
            elif izbira.lower() == "n":
                self.menu = "izpisRacunov"
            self.menu = "izpisRacunov"

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
            transakcije = modli.transakcije(self.racun)
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

