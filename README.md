Django HTTP Reporting API
=========================

Django-based API endpoint for receiving incident reports from [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSP), [HTTP Public Key Pinning](https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning) (HPKP), and the forthcoming [HTTP Reporting API](https://wicg.github.io/reporting/).

Note: This project does not attempt to enable reporting.

## Install

**Warning: This project is not yet on PyPI, so these instructions aren't functional.**

```bash
pip install Django-HTTP-Reporting-API
```

Add the app to your Django project's `settings.py`:

```python
INSTALLED_APPS = [
	...
	'http_reporting_api',
	...
]
```

And in `urls.py`:

```python
urlpatterns = [
	...
	# Django HTTP Reporting API
	url(r'^reporting', include('http_reporting_api.urls')),
	...
]
```

Run the database migration:

```bash
./manage.py migrate http_reporting_api
```

## Configure

Configure logging in `settings.py`:

```python
LOGGING = {
	...
	'handlers': {
		...
		'http_reporting': {
			'class': 'http_reporting_api.logging.DatabaseLogHandler'
		}
	},
	...
	'loggers': {
		...
		'http_reporting_api': {
			'handlers': ['http_reporting'],
			'propagate': False
		}
	}
}
```
