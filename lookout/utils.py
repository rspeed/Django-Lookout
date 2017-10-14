

class attribute (property):
	""" Decorator similar to @property, but for class attributes. """

	def __get__(self, instance, owner=None):
		return self.fget.__get__(None, owner)()

	def __set__(self, obj, value):
		super().__set__(type(obj), value)

	def __delete__(self, obj):
		super().__delete__(type(obj))
