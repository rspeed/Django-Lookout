"""
URL patterns for the API endpoint.

Add the endpoint to your ``urls.py`` like so:

.. code:: python

	urlpatterns = [
		...
		# Django Lookout
		url(r'^reporting', include('lookout.urls')),
		...
	]
"""

from django.conf.urls import url

from .views import ReportView


app_name = 'lookout'
urlpatterns = [
	url(r'^$', ReportView.as_view(), name='http-report'),
]
