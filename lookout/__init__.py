from pkg_resources import get_distribution, DistributionNotFound
from os import path



def package_version():
	""" Attempts to determine the package's version. """

	# VERSION.txt
	try:
		with open(path.join(path.dirname(__file__), 'VERSION.txt')) as version_file:
			return version_file.read().strip()
	except (FileNotFoundError, PermissionError):
		# Probably a development environment
		pass

	# pkg_resources
	try:
		return get_distribution('Django-Lookout').version
	except DistributionNotFound:
		# The package isn't installed
		pass

	return None


__version__ = package_version()

default_app_config = '{}.apps.ReportURIConfig'.format(__name__)
