Django Lookout
==============

Django-based API endpoint for receiving incident reports from [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) (CSP), [HTTP Public Key Pinning](https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning) (HPKP), and the forthcoming [HTTP Reporting API](https://wicg.github.io/reporting/).

Note: This project does not attempt to enable reporting.

## Install

**Warning: This project is not yet on PyPI, so these instructions aren't functional.**

```bash
pip install Django-Lookout
```

Add the app to your Django project's `settings.py`:

```python
INSTALLED_APPS = [
	...
	'lookout',
	...
]
```

And in `urls.py`:

```python
urlpatterns = [
	...
	# Django Lookout
	url(r'^reporting', include('lookout.urls')),
	...
]
```

Run the database migration:

```bash
./manage.py migrate lookout
```

## Configure

Configure logging in `settings.py`:

```python
LOGGING = {
	...
	'handlers': {
		...
		'lookout_db': {
			'class': 'lookout.logging.DatabaseLogHandler'
		}
	},
	...
	'loggers': {
		...
		'lookout': {
			'handlers': ['lookout_db'],
			'propagate': False
		}
	}
}
```
