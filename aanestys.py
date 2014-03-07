# coding=utf-8

from bottle import route, run, template

@route('/hello/<name>')
def index(name):
    return template('aanestys_template',name=name)

run(host='localhost', port=8080)
