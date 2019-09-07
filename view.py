from bottle import Bottle, run, view, request, redirect
import bottle
import sys
from model import Table
from beaker.middleware import SessionMiddleware
import re

session_opts = {
    'session.type': 'file',
    'session.cookie_expires': 300,
    'session.data_dir': './data',
    'session.auto': True
}


#app = Bottle()
app = SessionMiddleware(bottle.app(), session_opts)

@bottle.route('/')
@view('start')
def hello():
    return dict()

@bottle.route('/generate', method='POST')
def click():
  s = bottle.request.environ.get('beaker.session')
  x = int(request.forms.get('size_x'))
  y = int(request.forms.get('size_y'))
  num = int(request.forms.get('num_mines'))
  t = Table(num,x,y)
  s['table'] = t
  s.save()
  redirect('/game')


@bottle.route('/game')
@view('table_template')
def table_view():
    s = bottle.request.environ.get('beaker.session')
    t = s.get('table',None)
    if t is None:
      t = Table(5,5,7)
      s['table'] = t
      s.save()
    return dict(table = t)

@bottle.route('/click', method='POST')
def click():
  print('This is standard output', file=sys.stdout)
  s = bottle.request.environ.get('beaker.session')
  t = s.get('table',None)
  if t is None:
    return table_view()

  postdata = request.body.read()
  print(postdata)
  xy = request.forms.get('button')

  for position in xy.split(","):
    if position is None:
      return  table_view()
  x = int(xy.split(",")[0])
  y = int(xy.split(",")[1])

  
  t.open_xy(x,y)
  s['table'] = t
  s.save()

  return table_view()


run(app, host='localhost', port=8080, reloader=True)
