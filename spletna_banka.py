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
from bottle import *

@get('/')
def glavniMenu():
    return template('glavni.html', ime = None, priimek = None, emso = None,
                        ulica = None, hisna_st = None, postna_st = None,
                        kraj = None, napaka = None)

@get('/static/<filename:path>')
def static(filename):
    return static_file(filename, root='static')

@get('/oseba/<emso>')
def oOsebi(emso):
    racuni = modeli.racunEMSO(emso)
    return template('oseba.html', emso = emso, racuni = racuni)

@get('/isci')
def isci():
    priimek = request.query.iskalniNiz
    rezultat = modeli.poisciPriimek(priimek)
    return template('isci.html', rezultat = rezultat)

@post('/dodaj')
def dodaj():
    emso = request.forms.emso
    ime = request.forms.ime
    priimek = request.forms.priimek
    ulica = request.forms.ulica
    hisna_st = request.forms.hisna_st
    postna_st = request.forms.postna_st
    kraj = request.forms.kraj
    try:
        if not modeli.dodajOsebo(ime, priimek, emso, ulica, hisna_st, postna_st):
            modeli.dodajKraj(postna_st, kraj)
            modeli.dodajOsebo(ime, priimek, emso, ulica, hisna_st, postna_st)
    except Exception as e:
        return template('glavni.html', ime = ime, priimek = priimek, emso = emso,
                        ulica = ulica, hisna_st = hisna_st, postna_st = postna_st,
                        kraj = kraj, napaka = e)
    redirect('/oseba/' + emso)

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080)
