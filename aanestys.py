#!/usr/bin/env python2
# coding=utf-8
from operator import getitem

import json

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

@post('/lisaa_aanestys')
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

def hae_aanestys(numero):
    for aanestys in aanestykset:
        if aanestys['numero'] == int(numero):
            return aanestys
    raise KeyError("Äänestystä ei löytynyt")

def aanesta(aani):
    numero = request.forms['numero']
    hae_aanestys(numero)[aani] += 1
    return redirect('/', 303)

@post('/aanesta_kylla')
def aanesta_kylla():
    return aanesta('kylla')

@post('/aanesta_ei')
def aanesta_ei():
    return aanesta('ei')

@post('/sulje_aanestys')
def sulje_aanestys():
    numero = request.forms['numero']
    hae_aanestys(numero)['suljettu'] = True
    return redirect('/', 303)

@route('/')
def aanestykset_raaka():
    return json.dumps(aanestykset, indent=2)

@route('/hello/<name>')
def index(name):
    return template('aanestys_template',name=name)

run(host='localhost', port=8080)
