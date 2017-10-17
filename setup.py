import subprocess
from os import path
from setuptools import setup, find_packages


# Root directory of the project
project_dir = path.dirname(__file__)


# Use pandoc to convert README.md to reStructuredText
try:
	pandoc = subprocess.run(
		[
			'pandoc',
			'--from=markdown_github',
			'--to=rst',
			'--columns=1000',
			'--wrap=none',
			path.join(path.abspath(project_dir), 'README.md')
		],
		stdout=subprocess.PIPE,
		check=True
	)

except (OSError, subprocess.CalledProcessError):
	print("pandoc isn't available")
	long_description = ''

else:
	long_description = pandoc.stdout.decode('utf-8')



setup(
	name='Django-Lookout',

	use_scm_version={'write_to': path.join(project_dir, 'lookout', 'VERSION.txt')},

	description='API endpoint for receiving incident reports from Content Security Policy (CSP), HTTP Public Key Pinning (HPKP), and the HTTP Reporting API.',
	long_description=long_description,
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
		'wheel'
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
