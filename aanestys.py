#!/usr/bin/env python2
# coding=utf-8
from operator import getitem

import json
import threading

from functools import wraps

from bottle import *

aanestykset = [
    {"numero": 1,
     "nimi": "Hassut hatut perjantaisin",
     "kylla": 10,
     "ei": 3,
     "suljettu": False},
    {"numero": 2,
     "nimi": "Leppä Suomen kuninkaaksi",
     "kylla": 14,
     "ei": 12,
     "suljettu": False},
    {"numero": 3,
     "nimi": "Vatsastapuhumisen VS-kurssin järjestäminen",
     "kylla": 3,
     "ei": 2,
     "suljettu": True}
]

lukko = threading.Lock()

def lukitse(f):
    @wraps(f)
    def lukittu(*args, **kwargs):
        with lukko:
            return f(*args, **kwargs)
    return lukittu

def hae_aanestys(numero):
    for aanestys in aanestykset:
        if aanestys['numero'] == int(numero):
            return aanestys
    raise KeyError("Äänestystä ei löytynyt")

def aanesta(aani):
    numero = request.forms['numero']
    hae_aanestys(numero)[aani] += 1
    return redirect('/', 303)

@post('/lisaa_aanestys', name='lisaa_aanestys')
@lukitse
def lisaa_aanestys():
    aanestykset.append(
        {
            "numero": max(getitem(x, 'numero') for x in aanestykset) + 1,
            "nimi": request.forms['nimi'],
            "kylla": 0,
            "ei": 0,
            "suljettu": False,
        }
    )
    return redirect('/', 303)

@post('/aanesta_kylla', name='aanesta_kylla')
@lukitse
def aanesta_kylla():
    return aanesta('kylla')

@post('/aanesta_ei', name='aanesta_ei')
@lukitse
def aanesta_ei():
    return aanesta('ei')

@post('/sulje_aanestys', name='sulje_aanestys')
@lukitse
def sulje_aanestys():
    numero = request.forms['numero']
    hae_aanestys(numero)['suljettu'] = True
    return redirect('/', 303)

@route('/')
def kaikki_aanestykset():
    return template('aanestys_template_2',
                    aanestykset=aanestykset,
                    get_url=app().get_url)

@route('/hello/<name>')
def index(name):
    return template('aanestys_template',name=name)

run(host='localhost', port=8888)
