""" Utilities for Django Lookout """

from typing import Optional, Callable



class ClassPropertyDescriptor:
	""" Descriptor for an object that acts similarly to @property, but for class attributes. """

	fget: (staticmethod, classmethod) = None
	fset: (staticmethod, classmethod) = None
	fdel: (staticmethod, classmethod) = None


	def __init__ (self, fget: Callable, fset: Optional[Callable]=None, fdel: Optional[Callable]=None):
		self.getter(fget)

		if fset is not None:
			self.setter(fset)

		if fdel is not None:
			self.deleter(fdel)


	def getter (self, fget: Callable):
		""" Acts like ``property.getter``. """
		if not isinstance(fget, (classmethod, staticmethod)):
			fget = classmethod(fget)

		self.fget = fget
		return self


	def setter (self, fset: Callable):
		""" Acts like ``property.setter``. """
		if not isinstance(fset, (classmethod, staticmethod)):
			fset = classmethod(fset)

		self.fset = fset
		return self


	def deleter (self, fdel: Callable):
		""" Acts like ``property.deleter``. """
		if not isinstance(fdel, (classmethod, staticmethod)):
			fdel = classmethod(fdel)

		self.fdel = fdel
		return self


	def __get__ (self, obj, object_type=None):
		if object_type is None:
			# The classproperty is being accessed on an instance
			object_type = type(obj)

		return self.fget.__get__(obj, object_type)()


	def __set__ (self, obj, value):
		if self.fset is None:
			raise AttributeError("Can't set attribute")

		# Call the classmethod-wrapped function
		return self.fset.__get__(obj, type(obj))(value)


	def __del__ (self, obj):
		if self.fdel is None:
			raise AttributeError("Can't delete attribute")

		return self.fset.__get__(obj, type(obj))()



def classproperty (fget: Callable) -> ClassPropertyDescriptor:
	""" Decorator similar to @property, but for class attributes. """

	if not isinstance(fget, (classmethod, staticmethod)):
		fget = classmethod(fget)

	return ClassPropertyDescriptor(fget)
