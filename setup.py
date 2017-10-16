from os import path
from setuptools import setup, find_packages


# Root directory of the project
project_dir = path.dirname(__file__)


# Dump the contents of README.md into a variable
with open(path.join(path.abspath(project_dir), 'README.md'), encoding='utf-8') as f:
	long_description = f.read()



class LazyMarkdownConverter:
	""" Lazily converts README from Markdown to reStructuredText using pandoc. """

	IN_FORMAT = 'markdown_github'
	OUT_FORMAT = 'rst'


	def __init__(self, value):
		self.value = value
		self.converted = False


	def __str__(self):
		""" Performs the conversion and caches the result. """

		if not self.converted:
			try:
				from pypandoc import convert_text
				self.value = convert_text(
					self.value,
					self.OUT_FORMAT,
					self.IN_FORMAT,
					extra_args=['--columns=1000', '--wrap=none']
				)
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
	name='Django-Lookout',

	use_scm_version={'write_to': path.join(project_dir, 'lookout', 'VERSION.txt')},

	description='API endpoint for receiving incident reports from Content Security Policy (CSP), HTTP Public Key Pinning (HPKP), and the HTTP Reporting API.',
	long_description=LazyMarkdownConverter(long_description),
	long_description_content_type='UTF-8',

	url='https://github.com/rspeed/Django-Lookout',

	author='Rob Speed',
	author_email='rspeed@bounteo.us',

	packages=find_packages(exclude=[
		'tests',
		'tests.*'
	]),
	package_data={
		'lookout': ['VERSION.txt']
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
		'Development Status :: 3 - Alpha',
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
	keywords='django csp hpkp security error-monitoring https'
)
