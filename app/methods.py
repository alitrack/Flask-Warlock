

#from flask_appbuilder import ImageManager


def __repr__(self):
	return self.name

def photo_img(self, g000, g001):#												||
	im = ImageManager()#														||
	if g001:#																	||
		data = {'url': url_for(url, pk=str(g000)), 'src': im.get_url(g001)}#	||
	else:#																		||
		data = {'url': url_for(url, pk=str(g000)), 'src': '//:0'}#				||
	markup = subtrix.mechanism(pxcfg['link_image']['text'],data).run()[0]#		||
	return Markup(markup)#														||

def photo_img_thumbnail(self, url, g000, g001):#								||
	im = ImageManager()#														||
	if g001:#																	||
		data = {'url': url_for(url, pk=str(g000)),#								||
											'src': im.get_url_thumbnail(g001)}#	||
	else:#																		||
		data = {'url': url_for(url, pk=str(g000)), 'src': '//:0'}#				||
	markup = subtrix.mechanism(pxcfg['link_image']['text'],data).run()[0]#		||
	return Markup(markup)#														||

def percentage(self, g000, g001):#												||
	''
	numerator = g000
	denominator = g001
	if denominator != 0:
		return (numerator*100)/denominator
	else:
		return 0.0

def month_year(self, g000):
	date = g000
	return datetime.datetime(date.year, date.month, 1)

def year(self, g000):
	date = g000
	return datetime.datetime(date.year, 1, 1)

def label(self):
	''
	pxcfg['strong']['text']
