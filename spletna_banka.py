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
    return template('glavni.html')

@get('/oseba')
def oOsebi():
    return template('oseba.html')

# poženemo strežnik na portu 8080, glej http://localhost:8080/
run(host='localhost', port=8080, reloader=True)
