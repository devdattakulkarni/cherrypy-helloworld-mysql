import os
import random

import cherrypy
from jinja2 import Environment, FileSystemLoader
import MySQLdb

ENV = Environment(loader=FileSystemLoader('templates'))


def get_params():
    params = {'dbname': os.environ.get('dbname', ''),
              'user': os.environ.get('user', ''),
              'password': os.environ.get('password', ''),
              'dbhost': os.environ.get('dbhost', '')}
    return params


class Root(object):
    @cherrypy.expose
    def index(self):
        tmpl = ENV.get_template('index.html')
        params = get_params()
        db = MySQLdb.connect(params['dbhost'],
                             params['user'],
                             params['password'],
                             params['dbname'])
        cursor = db.cursor()
        sql = "SELECT * FROM people"

        try:
            cursor.execute(sql)
            results = cursor.fetchall()
            name = random.choice(results)
            names = {}
            names['name'] = name
        except:
            print "Error: unable to fecth data"

        return tmpl.render(names)

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                        'server.socket_port': int(os.environ.get('PORT',
                                                                 '8055'))})

cherrypy.quickstart(Root())
