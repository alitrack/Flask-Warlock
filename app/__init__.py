import logging

from flask import Flask
from flask_appbuilder import AppBuilder, SQLA
""" Logging configuration"""
logging.basicConfig(format="%(asctime)s:%(levelname)s:%(name)s:%(message)s")
logging.getLogger().setLevel(logging.DEBUG)

#build custom flask override template loading
class Yask(Flask):
	def __init__(self):
		Flask.__init__(self, __name__)
		self.jinja_loader = jinja2.ChoiceLoader([self.jinja_loader, jinja2.PrefixLoader({}, delimiter = ".")])#	||
	def create_global_jinja_loader(self):
		return self.jinja_loader
	def register_blueprint(self, bp):
		Flask.register_blueprint(self, bp)
		self.jinja_loader.loaders[1].mapping[bp.name] = bp.jinja_loader

app = Flask(__name__)
app.config.from_object("config")
db = SQLA(app)
appbuilder = AppBuilder(app, db.session, base_template='appbase.html')

from . import views

'''
http://fewstreet.com/2015/01/16/flask-blueprint-templates.html
'''
