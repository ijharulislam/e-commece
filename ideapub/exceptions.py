# ideapub exceptions



class IdeapubError (Exception):
	def __init__ (self, *args, **kwargs):
		super (IdeapubError, self).__init__(*args, **kwargs)