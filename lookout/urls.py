from django.conf.urls import url

from .views import ReportView


app_name = 'lookout'
urlpatterns = [
	url(r'^$', ReportView.as_view(), name='http-report'),
]
