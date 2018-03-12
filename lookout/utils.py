""" Utilities for Django Lookout """

from typing import Union, Callable, Any



class classproperty:
	"""
	Decorator & descriptor for objects that act similarly to @property, but for class attributes.
	Due to limitations of class attributes, only the getter is easily implemented.
	"""

	fget: Union[staticmethod, classmethod] = None
	""" The wrapped getter function. """


	def __init__ (self, fget: Callable) -> None:
		if not isinstance(fget, (classmethod, staticmethod)):
			fget = classmethod(fget)
		self.fget = fget


	def __get__ (self, obj, owner=None) -> Any:
		if self.fget is None:
			raise AttributeError("Can't get attribute")

		if owner is None:
			# The classproperty is being accessed on an instance
			owner = type(obj)

		# Call the wrapped function
		return self.fget.__get__(obj, owner)()
