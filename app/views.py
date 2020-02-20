
from importlib import import_module
import sys, inspect
from os.path import abspath, dirname, join#										||
#===============================================================================||
from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import BaseView, ModelView, ModelRestApi, expose, has_access
#===============================================================================||
from . import appbuilder, db

from app.util import getYAML, thingify
#===============================================================================||
from pheonix.elements.config import config#										||
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
#===============================================================================||
cfg = config.instruct('{0}config.yaml'.format(here)).load().dikt#				||
print('CFG Keys',cfg.keys())
site = [x for x in cfg['modules'].keys() if cfg['modules'][x]['active'] == 1]
bps = config.instruct('{0}models.yaml'.format(here)).load().dikt['models']#		||
for bp in bps.keys():#															||
	if not isinstance(bps[bp], dict) or bp not in site:#						||
		continue#																||
	for model in bps[bp]:#														||
		module = import_module('app.models')#									||
		try:
			globals()[model] = getattr(module, model)#							||
		except:
			pass
#===============================================================================||
cfg = config.instruct('{0}views.yaml'.format(here)).load().dikt#				||
def buildViews():#																||
	for bp in cfg['modelViews'].keys():#												||
		if not isinstance(cfg['modelViews'][bp], dict) or bp not in site:#			||
			continue#															||
		for view, vwcfg in cfg['modelViews'][bp].items():#							||
			baseVIEW = thingify(vwcfg['viewtype'])#								||
			vclass = ViewFactory(view, vwcfg, baseVIEW)#						||
			if vclass == None:#													||
				continue#														||
			globals()[view] = vclass#											||
def ViewFactory(name, cfg, BaseClass):#											||
	if cfg['viewtype'] == 'flask_appbuilder.BaseView':#							||
		kwargs = {}#															||
		cnt = 0#																||
		for method in cfg['methods']:#											||
			kwargs[method] = FxFactory(cfg['methods'][method])#					||
			if cnt == 0:#														||
				kwargs['default_view'] = method#								||
			cnt += 1#															||
			def method(self, cfg):#												||
				for var in cfg.keys():#											||
					locals()[var] = cfg[var]#									||
				self.update_redirect()#											||
				return self.render(template(tmplt), **kwargs)
		newclass = type(name, (BaseClass, ), {**kwargs})#						||
	elif cfg['viewtype'] == 'flask_appbuilder.ModelView':#						||
		def __init__(self):#													||
			BaseClass.__init__(self)#											||
		datamodel = setModelViewVars(cfg)#							||
		if datamodel == None:#								||
			return None#								||
		datamodel = datamodel['datamodel']#								||
		newclass = type(name, (BaseClass,),{"__init__": __init__,#				||
											'datamodel': datamodel})#			||
	elif cfg['viewtype'] == 'flask_appbuilder.charts.views.DirectByChartView':#	||
		datamodel = setModelViewVars(cfg)['datamodel']
		chart_title = cfg['chart_title']#										||
		definitions = cfg['definitions']#										||
	elif cfg['viewtype'] == 'flask_appbuilder.charts.views.GroupByChartView':#	||
		chart_title = cfg['chart_title']#										||
		definitions = cfg['definitions']#										||
	else:#																		||
		print(cfg['viewtype'], 'Not Valid')#									||
	return newclass#															||
def FxFactory(cls, cfg):#														||
	args, kwargs = cfg['args'], cfg['kwargs']#									||
	@expose(cfg['decorators']['expose'])#										||
	def function_template(args, kwargs):#										||
		for arg in args:#														||
			pass#								||
	return function_template#													||
def setModelViewVars(cfg):#														||
	kwargs = {}#																||
	try:#								||
		interface = thingify(cfg['datamodel']['interface'])#					||
		model = thingify(cfg['datamodel']['model'])#							||
	except:#								||
		return None#								||
	kwargs['datamodel'] = interface(model)#										||
	return kwargs#																||
@appbuilder.app.errorhandler(404)#								||
def page_not_found(e):#								||
    return (render_template("404.html", base_template=appbuilder.base_template,
												appbuilder=appbuilder),404,)#	||
def ViewRegistrationFactory(cfg, viewType):#												||
	for bp, views in cfg.items():#											||
		if not isinstance(views, dict) or bp not in site:#										||
			continue#															||
		for view, params in views.items():#										||
			if view == 'SimpleView0':#											||
				continue#														||
			rvcfg = params['registration']#										||
			if viewType == 'ModelView':
				try:#																||
					appbuilder.add_view(thingify(rvcfg['class']), rvcfg['title'],#	||
															**rvcfg['kwargs'])#	||
				except:#															||
					continue#														||
			elif viewType == 'PageView':
				try:#																||
					appbuilder.add_view(thingify(rvcfg['class']),
											rvcfg['title'], **rvcfg['kwargs'])#	||
					appbuilder.add_link(thingify())
				except:#															||
					continue#														||
db.create_all()#																||
buildViews()#																	||
ViewRegistrationFactory(cfg['modelViews'], 'ModelView')#						||

class pyAutodExcel(BaseView):
	default_view = 'index'
	@expose('/', methods=['GET',])
#	@has_access
	def index(self):
		return self.render_template("testPage.html")#				||
	@expose('/<seq>', methods=['GET',])
#	@has_access
	def Seq000(self, seq):
		return self.render_template("testPage.html", param1=seq)#				||
	@expose('/seq001', methods=['GET',])
#	@has_access
	def Seq001(self):
		return self.render_template("testPage.html")#							||
	@expose('/seq002', methods=['GET',])
	def Seq002(self):
		return self.render_template("tabs.html")
appbuilder.add_view(pyAutodExcel, "index", category='Software', category_icon='fa-envelope', icon='fa-envelope', label='Guides')
appbuilder.add_link("Seq000", href='/pyautodexcel/seq000', category='Software', icon='fa-envelope', label='Lessons')
appbuilder.add_link("Seq001", href='/pyautodexcel/seq001', category='Software', icon='fa-envelope', label='Lessons1')
appbuilder.add_link("Seq002", href='/pyautodexcel/seq002', category='Software', icon='fa-envelope', label='Lessons2')
class cal(BaseView):
	default_view = 'index'
	@expose('/', methods=['GET',])
	def index(self):
		return self.render_template('calendar.calendar.html')
appbuilder.add_view(cal, "index", category='Calendar', category_icon='fa-envelope', icon='fa-envelope', label='Month')

























#create a pull down listing the lessons?
