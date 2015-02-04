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
    #params = {'dbname': 'arbor_demo',
    #          'user': 'demo',
    #          'password': 'demo_2014',
    #          'dbhost': '97f8f462ee7e1c3b7ffeb448db096c7ec3ec8233.rackspaceclouddb.com'}
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
