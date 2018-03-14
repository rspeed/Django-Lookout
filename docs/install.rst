Install and Configure
=====================

.. warning::  If you're using HPKP, Django Lookout *must* be set up `on a different domain name <https://developers.google.com/web/updates/2015/09/HPKP-reporting-with-chrome-46#one_last_gotcha>`_.


Step 1: Install
~~~~~~~~~~~~~~~

.. code:: bash

	pip install Django-Lookout


Step 2: Update ``INSTALLED_APPS``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the app to your project's ``settings.py``:

.. code:: python

	INSTALLED_APPS = [
		...
		'lookout',
		...
	]


Step 3: Configure the API Endpoint
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the API endpoint to ``urls.py``. This is where you'll point ``report-uri`` on the frontend.

.. note:: You can set the pattern to whatever you want.
.. note:: Be mindful of trailing slashes.

.. code:: python

	urlpatterns = [
		...
		# Django Lookout
		url(r'^reporting', include('lookout.urls')),
		...
	]


Step 4: Migrate
~~~~~~~~~~~~~~~

Run the database migrations:

.. code:: bash

	./manage.py migrate lookout


Step 5: Configure CSP/HPKP
~~~~~~~~~~~~~~~~~~~~~~~~~~

[To do]

.. todo:: Suggest ways to set up CSP/HPKP.
