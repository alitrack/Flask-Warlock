#@@@@@@@@@@@@@@@@@@@ Beaver ngynFlask App Greenprints @@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name: #																		||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#===============================Core Modules====================================||
from flask import Blueprint, render_template, current_app as app#				||
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import ModelRestApi, AppBuilder, expose, has_access
from app import appbuilder, db
from flask_appbuilder import Model
from sqlalchemy import Column, Date, Float, ForeignKey, Integer, String
from flask_appbuilder.models.mixins import ImageColumn
from sqlalchemy.orm import relationship
#===============================================================================||
from app.util import getYAML
#===============================================================================||
from pheonix.organisms.monk import monk
from pheonix.elements.thing.thing import thingify
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
#===============================================================================||
#--------Blue Print Factory ----------------------------------------------------||
admin_bp = Blueprint('admin_bp', __name__, template_folder='templates',#		||
													static_folder='static')#	||
def buildBluePrints():
	''
	cfg = monk.stone('app/blueprint.yaml').dikt
def BlueprintFactory(package):#													||
	for blueprint in package:#													||
		args = package[blueprint]['args']#										||
		args.append(__name__)#													||
		kwargs = package[blueprint]['kwargs']#									||
		globals()[blueprint] = Blueprint(*args, **kwargs)#						||
def bpRegistrationFactory():#														||
	''#													||
	for bprint in package:#														||
		app.register_bluprint(thingify(package[bprint['registration']]))#		||
buildBluePrints()
#--------Form Factory ----------------------------------------------------------||
def buildForms():
	cfg = monk.stone('app/forms.yaml').dikt
	print('Build Model Config',cfg)
	for form in cfg['forms'].keys():
		globals()[form] = ModelFactory(model, cfg['forms'][form], Form)#		||
def FormFactory(name, cfg, BaseClass=FlaskForm):#								||
	def __init__(self, cfg):
		BaseClass.__init__(self, name[:-len("Class")])
	def __repr__(self):
		return self.name
	kwargs = setFormVars(cfg)
	newclass = type(name, (BaseClass,),{"__init__": (__init__, cfg),#			||
											'__repr__': __repr__, **kwargs})#	||
	return newclass
def setFormVars(cfg):#															||
	kwargs = {}#																||
	print('Columns', cfg)#														||
	for col in cfg['columns'].keys():#											||
		params = collapse(cfg['columns'][col])#									||
		if params['size'] == None:#												||
			value = Column(thingify(params['type']), **params['kwargs'])#		||
		else:
			value = Column(thingify(params['type'])(int(params['size'])),#		||
														**params['kwargs'])#	||
		kwargs[col] = value
	return kwargs
buildForms()
#--------Model Factory ---------------------------------------------------------||
def buildModels():
	cfg = monk.stone('app/models.yaml')
	print('Build Model Config',cfg.configs)
	for model in cfg.configs['models'].keys():
		globals()[model] = ModelFactory(model, cfg['models'][model], Model)
def ModelFactory(name, cfg, BaseClass=Model):
	def __init__(self, cfg):
		BaseClass.__init__(self, name[:-len("Class")])
	def __repr__(self):
		return self.name
	kwargs = setModelVars(cfg)
	newclass = type(name, (BaseClass,),{"__init__": (__init__, cfg),
											'__repr__': __repr__, **kwargs})#	||
	return newclass
def setModelVars(cfg):
	kwargs = {}
	print('Columns', cfg)
	for col in cfg['columns'].keys():
		params = collapse(cfg['columns'][col])
		if params['size'] == None:
			value = Column(thingify(params['type']), **params['kwargs'])
		else:
			value = Column(thingify(params['type'])(int(params['size'])),#		||
														**params['kwargs'])#	||
		kwargs[col] = value
	return kwargs
def collapse(params):
	'Combine Model Arguments from Parameters'
	p = params['dargs']
	if params['oargs'] == None:
		return p
	for key in params['oargs'].keys():
		p[key] = params['oargs'][key]
	return p
buildModels()
#--------View Factory ----------------------------------------------------------||
def buildViews():#														||
	cfg = getYAML('app/views.yaml')#									||
	for view in cfg['views'].keys():#									||
		baseVIEW = thingify(cfg['views'][view]['viewtype'])#			||
		vcfg = cfg['views'][view]#										||
		globals()[view] = ViewFactory(view, vcfg, baseVIEW)#			||
def ViewFactory(name, cfg, BaseClass):#									||
	if cfg['viewtype'] == 'flask_appbuilder.BaseView':#					||
		kwargs = {}
		cnt = 0
		for method in cfg['methods']:
			kwargs[method] = FxFactory(cfg['methods'][method])
			if cnt == 0:
				kwargs['default_view'] = method
			cnt += 1
			def method(self, cfg):
				for var in cfg.keys():
					locals()[var] = cfg[var]
				self.update_redirect()
				return self.render(template(tmplt), **kwargs)
		newclass = type(name, (BaseClass, ), {**kwargs})#				||
	elif cfg['viewtype'] == 'flask_appbuilder.ModelView':#				||
		def __init__(self):#											||
			BaseClass.__init__(self)#									||
		datamodel = setModelViewVars(cfg)['datamodel']#						||
		newclass = type(name, (BaseClass,),{"__init__": __init__,#		||
											'datamodel': datamodel})#	||
	elif cfg['viewtype'] == 'flask_appbuilder.charts.views.DirectByChartView':#				||
		datamodel = setModelViewVars(cfg)['datamodel']
		chart_title = cfg['chart_title']
		definitions = cfg['definitions']
	elif cfg['viewtype'] == 'flask_appbuilder.charts.views.GroupByChartView':#				||
		chart_title = cfg['chart_title']
		definitions = cfg['definitions']
	else:
		print(cfg['viewtype'])
	return newclass#													||
def FxFactory(cls, cfg):
	args, kwargs = cfg['args'], cfg['kwargs']
	@expose(cfg['decorators']['expose'])
	def function_template(args, kwargs):
		for arg in args:
			#locals()[arg]
			pass
	return function_template
def setBaseViewVars(cfg):
	print('Cfg', cfg)
	kwargs = {}
def setModelViewVars(cfg):#												||
	kwargs = {}#														||
	interface = thingify(cfg['datamodel']['interface'])#				||
	model = thingify(cfg['datamodel']['model'])#						||
	kwargs['datamodel'] = interface(model)#								||
	return kwargs#														||
buildViews()#															||
@appbuilder.app.errorhandler(404)#										||
def page_not_found(e):#													||
	return (render_template("404.html",#								||
								base_template=appbuilder.base_template,#||
								appbuilder=appbuilder), 404,)# 			||

db.create_all()
def viewRegistrationFactory():
	cfg = getYAML('app/views.yaml')
	for view, vcfg in cfg['views'].items():
		if view == 'SimpleView0':
			continue
		rvcfg = vcfg['registration']
		appbuilder.add_view(thingify(rvcfg['class']), rvcfg['title'],#	||
													**rvcfg['kwargs'])#	||
viewRegistrationFactory()
