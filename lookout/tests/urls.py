from django.conf.urls import include, url


urlpatterns = [
	url(r'^report', include('lookout.urls')),
]
