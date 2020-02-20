#===============================Core Modules====================================||
from os.path import abspath, dirname, join#										||
import sys, inspect
#===============================================================================||
from flask_appbuilder import Model

#from flask_appbuilder.base.mixins.filemanager import ImageManager

from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
#=======================================================================||
from app.util import getYAML, thingify
from app import methods
from pheonix.elements.config import config#										||
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
#===============================================================================||
cfg = config.instruct('{0}config.yaml'.format(here)).load().dikt#				||
site = [x for x in cfg['modules'].keys() if cfg['modules'][x]['active'] == 1]
def buildModels():
	cfg = config.instruct('{0}models.yaml'.format(here)).load().dikt#			||
	print('CFG',cfg)
	for bp in cfg['models'].keys():
		if not isinstance(cfg['models'][bp], dict) or bp not in site:
			continue
		for model, mdlcfg in cfg['models'][bp].items():
			print('Model',model)
			globals()[model] = ModelFactory(model, mdlcfg, Model)
def ModelFactory(name, cfg, BaseClass=Model):
	def __repr__(self):
		return self.name
	kwargs = setModelVars(cfg['columns'])
#	methods = setModelMethods(cfg['methods'], self)
#need to go through dynamic assignment notes and fix this to work properly
	newclass = type(name, (BaseClass,), {'__repr__': __repr__, **kwargs})#	||
	return newclass
def setModelMethods(cfg, self):
	''
	addMethods = {'__repr__': __repr__}
	for method in methods:
		if method in methods.__dir__():
			addMethods[method] = method(self)
	return addMethods
def setModelVars(cfg):
	''
	kwargs = {}
	for col in cfg.keys():
		params = collapse(cfg[col])
		if params['size'] == None:
			value = Column(thingify(params['type']), **params['kwargs'])
		else:
			value = Column(thingify(params['type'])(int(params['size'])), **params['kwargs'])
		kwargs[col] = value
	return kwargs
def collapse(params):
	p = params['dargs']
	if params['oargs'] == None or params['oargs'] == '':
		return p
	for key in params['oargs'].keys():
		p[key] = params['oargs'][key]
	return p
def printClasses():
	for name, obj in inspect.getmembers(sys.modules[__name__]):
		if inspect.isclass(obj):
			print(obj)
			print(vars(obj))
buildModels()
