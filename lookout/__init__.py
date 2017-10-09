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

	# setuptools_scm
	try:
		from setuptools_scm import get_version

		return get_version(get_version(root='..', relative_to=__file__))
	except ImportError:
		# That's not installed either!
		pass

	return 0


__version__ = package_version()

default_app_config = '{}.apps.ReportURIConfig'.format(__name__)
