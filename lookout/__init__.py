from typing import Optional
from pkg_resources import get_distribution, DistributionNotFound
from os import path



class PackageVersion:
	""" Attempts to determine the package's version. """

	__version = None


	def __new__(cls, *args, **kwargs):
		return cls.get()


	@classmethod
	def get (cls) -> str:
		""" Attempts each method to get the package version in turn until one succeeds. """

		return cls.from_file() or cls.from_distribution() or 'unknown'


	@staticmethod
	def from_file () -> Optional[str]:
		""" Gets the package version from the VERSION.txt file created by ``setuptools-scm``. """

		try:
			with open(path.join(path.dirname(__file__), 'VERSION.txt')) as version_file:
				return version_file.read().strip()
		except (FileNotFoundError, PermissionError):
			# Probably a development environment
			return None


	@staticmethod
	def from_distribution () -> Optional[str]:
		""" Gets the package version from its installed distribution using ``pkg_resources``. """

		try:
			return get_distribution('Django-Lookout').version
		except DistributionNotFound:
			# The package isn't installed
			return None



__version__ = PackageVersion()

default_app_config = '{}.apps.DjangoLookoutConfig'.format(__name__)
