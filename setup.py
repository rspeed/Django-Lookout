from os import path
from setuptools import setup, find_packages



class LazyReadmeConverter:
	""" Uses pandoc to convert the README from Markdown to reStructuredText. """

	IN_FORMAT = 'md'
	OUT_FORMAT = 'rst'
	converted = False


	def __init__(self, file_path):
		# Read the entire file contents into a string
		with open(file_path, encoding='utf-8') as f:
			self.value = f.read()


	def __str__(self):
		""" Performs the conversion and caches the result. """

		if not self.converted:
			try:
				from pypandoc import convert_text
				self.value = convert_text(self.value, self.OUT_FORMAT, self.IN_FORMAT)
			except ImportError:
				print("pypandoc isn't installed")
			except OSError:
				print("pandoc isn't available")
			finally:
				# No need to try more than once
				self.converted = True

		return self.value


	def __getattr__ (self, name):
		""" Wraps the converted value. """

		return getattr(str(self), name)


	def __repr__(self):
		""" Manually overloaded because it's special-cased by builtins. """

		return repr(str(self))



setup(
	name='Django-HTTP-Reporting-API',

	use_scm_version={'write_to': 'http_reporting_api/VERSION.txt'},

	description='API endpoint for receiving incident reports from Content Security Policy (CSP), HTTP Public Key Pinning (HPKP), and the HTTP Reporting API.',
	long_description=LazyReadmeConverter(path.join(path.abspath(path.dirname(__file__)), 'README.md')),

	url='https://github.com/rspeed/Django-HTTP-Reporting-API',

	author='Rob Speed',
	author_email='rspeed@bounteo.us',

	packages=find_packages(exclude=[
		'tests',
		'tests.*'
	]),
	package_data={
		'http_reporting_api': ['VERSION.txt']
	},
	include_package_data=True,

	install_requires=[
		'Django',
		'Pygments',
		'jsonschema',
		'pytz'
	],
	setup_requires=[
		'setuptools_scm',
		'pypandoc'
	],
	extras_require={
	},
	python_requires='>=3.5',

	license='MIT',
	classifiers=[
		'Development Status :: 2 - Pre-Alpha',
		'Environment :: Web Environment',
		'Framework :: Django :: 1.10',

		'Intended Audience :: Developers',
		'Intended Audience :: Information Technology',

		'License :: OSI Approved :: MIT License',

		'Natural Language :: English',

		'Programming Language :: Python :: 3.5',
		'Programming Language :: Python :: 3.6',

		'Topic :: Internet :: WWW/HTTP :: Site Management',
		'Topic :: Security',
		'Topic :: Security :: Cryptography',
		'Topic :: System :: Logging',
		'Topic :: System :: Monitoring',
	],
	keywords='https csp hpkp error notification'
)
