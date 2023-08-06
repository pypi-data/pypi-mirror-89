import webbrowser as _wbr
class CloseError(OSError):
	pass
class AlreadyClosedError(CloseError):
	pass
class IsClosedError(CloseError):
	pass
class Tag:
	def __init__(self,tag,**attrs):
		self.tag=tag
		self.attrs=attrs
		self.content=''
		self.closed=False
	def write(self,content):
		if not self.closed:
			self.content+=content
		else:
			attrstr=' '
			for i in self.attrs:
				attrstr+=i+'="'+self.attrs[i]+'" '
			attrstr=attrstr.rstrip()
			raise IsClosedError('<'+self.tag+attrstr+'> is closed')
	def close(self):
		if not self.closed:
			self.closed=True
		else:
			attrstr=' '
			for i in self.attrs:
				attrstr+=i+'="'+self.attrs[i]+'" '
			attrstr=attrstr.rstrip()
			raise AlreadyClosedError('already closed <'+self.tag+attrstr+'>')
	def _out(self):
		attrstr=' '
		for i in self.attrs:
			attrstr+=i+'="'+self.attrs[i]+'" '
		attrstr=attrstr.rstrip()
		return '<'+self.tag+attrstr+'>'+self.content+'</'+self.tag+'>'
class HTML(Tag):
	def __init__(self,intag='html'):
		super(HTML,self).__init__(intag)
	def open(self,tag):
		return HTML(intag=tag)
	def commit(self,tag):
		self.content+=tag._out()
	def output(self):
		return self._out()
	def open_in_browser(self):
		_wbr.open(f'data:text/html,{self.output()}')