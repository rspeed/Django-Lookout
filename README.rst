Django Lookout
==============

|build status|

|logo|

.. |build status| image:: https://travis-ci.org/rspeed/Django-Lookout.svg?branch=master
		:alt: Build Status
		:target: https://travis-ci.org/rspeed/Django-Lookout
.. |logo| image:: https://github.com/rspeed/Django-Lookout/raw/master/lookout/docs/logo.svg?sanitize=true
		:alt: Django Lookout logo: a lookout tower

Django Lookout is an API endpoint for collecting and processing automatic incident reports send by your visitors' web browsers. Currently that includes both `Content Security Policy <https://en.wikipedia.org/wiki/Content_Security_Policy>`__ (CSP) and `HTTP Public Key Pinning <https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning>`__ (HPKP), but support for additional report types is planned.

Before getting started you should familiarize yourself with the standards and their potential pitfalls (`especially HPKP <https://www.smashingmagazine.com/be-afraid-of-public-key-pinning/>`__). The risks can be mitigated significantly by using Django Lookout along with report-only policies, which would still allow you to be notified of potential attacks without the risk of accidentally rendering your web site inaccessible.

It's important to note that Django Lookout only handles the *reporting* part of the process. Setting the headers which tell browsers what to do, or even where to send reports, is outside its scope. You'll need to set the ``report-uri`` property for CSP and/or HPKP to point to your Django Lookout endpoint.



Install and Configure
---------------------

.. warning::  If you're using HPKP, Django Lookout *must* be set up on a different domain name.


Step 1
~~~~~~

.. code:: bash

	pip install Django-Lookout

Add the app to your Django project's ``settings.py``:

.. code:: python

	INSTALLED_APPS = [
		...
		'lookout',
		...
	]


Step 2
~~~~~~

Add the API endpoint to ``urls.py``.

.. note:: You can set the pattern to whatever you want. That's where you'll be pointing ``report-uri``.
.. note:: Be mindful of trailing slashes.

.. code:: python

	urlpatterns = [
		...
		# Django Lookout
		url(r'^reporting', include('lookout.urls')),
		...
	]


Step 3
~~~~~~

Run the database migrations:

.. code:: bash

	./manage.py migrate lookout



Standards
---------


Currently Supported
~~~~~~~~~~~~~~~~~~~

`Out-of-Band Reporting API <https://wicg.github.io/reporting/>`__
	A generic incident reporting API that can be used by all of the following standards. Django Lookout automatically converts reports using "legacy" schemas to the generic schema.

`Content Security Policy <https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP>`__
	Browsers will (optionally) block unauthorized content and send an incident report if a resource is requested which isn't permitted by the policy.

`HTTP Public Key Pinning <https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning>`__
	Browsers supporting HPKP will (optionally) block connections and send an incident report if the site doesn't use the specified HTTPS certificate in the future.


Planned Support
~~~~~~~~~~~~~~~

These standards are planned to be supported in Django Lookout 1.0:

`Network Error Logging <http://wicg.github.io/network-error-logging/>`__
	Browsers supporting NEL will send incident reports if a networking error is encountered when requesting content.

`Expect-CT <https://tools.ietf.org/html/draft-ietf-httpbis-expect-ct-02>`__
	Browsers supporting Report-CT will send an incident report if it receives a certificate which doesn't adhere to `Certificate Transparency <https://www.certificate-transparency.org/>`__ guidelines.

`Expect-Staple <https://scotthelme.co.uk/ocsp-expect-staple/>`__
	Browsers supporting Expect-Staple will send an incident report if a TLS handshake with the site doesn't include an `OCSP response <https://en.wikipedia.org/wiki/OCSP_stapling>`__.


Browser Implementation Status
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The only standard currently supported across all major browsers is Content Security Policy. It's hoped that the generic Out-of-Band Reporting API will significantly improve the situation in the future.

.. note:: This table only considers a feature supported if it includes reporting functionality.
.. note:: Internet Explorer is excluded due to the fact that it doesn't support any of these features via standard headers.

==================================  =======================  =======================  =======================  ==================
Standard                            Chrome                   Firefox                  Edge                     Safari
==================================  =======================  =======================  =======================  ==================
**Content Security Policy (CSP)**   Supported                Supported                Supported [#ecsp]_       Supported [#scsp]_
**HTTP Public Key Pinning (HPKP)**  Supported [#chpkp]_      Not Supported [#fhpkp]_  Not Supported [#ehpkp]_  Not Supported
**Out-of-Band Reporting API**       Not Supported [#cgapi]_  Not Supported            Not Supported            Not Supported
**Network Error Logging (NEL)**     Not Supported [#cnel]_   Not Supported            Not Supported [#enel]_   Not Supported
**Expect-CT**                       Supported [#cect]_       Not Supported [#fect]_   ?                        ?
**Expect-Staple**                   ?                        ?                        ?                        ?
==================================  =======================  =======================  =======================  ==================



Additional Information
----------------------


Content Security Policy
~~~~~~~~~~~~~~~~~~~~~~~

-  `Google Web Fundamentals – Content Security Policy <https://developers.google.com/web/fundamentals/security/csp/>`__
-  `Content Security Policy - An Introduction <https://scotthelme.co.uk/content-security-policy-an-introduction/>`__


HTTP Public Key Pinning
~~~~~~~~~~~~~~~~~~~~~~~

-  `Google – Rolling out Public Key Pinning with HPKP Reporting <https://developers.google.com/web/updates/2015/09/HPKP-reporting-with-chrome-46>`__
-  `Guidance on setting up HPKP <https://scotthelme.co.uk/guidance-on-setting-up-hpkp/>`__


Tools and Similar Projects
~~~~~~~~~~~~~~~~~~~~~~~~~~

-  `Observatory by Mozilla <https://observatory.mozilla.org/>`__. General website security testing suite.
-  `securityheaders.io <https://securityheaders.io>`__. Testing suite for security-related HTTP response headers.
-  `django-csp-reports <https://github.com/adamalton/django-csp-reports>`__. A similar project specifically for CSP reports.
-  `report-uri.io <https://report-uri.io/>`__. A commercial service which serves a similar purpose. They also have some useful free testing tools.



.. rubric:: Footnotes

..  [#ecsp] `Supported as of build 15002 <https://developer.microsoft.com/en-us/microsoft-edge/platform/status/contentsecuritypolicylevel2/>`__
..  [#scsp] `Unknown when support was added <https://webkit.org/status/#specification-content-security-policy-level-2>`__

..  [#chpkp] `Supported as of Chrome 46 <https://www.chromestatus.com/feature/4669935557017600>`__
..  [#fhpkp] `No support for report-uri <https://bugzilla.mozilla.org/show_bug.cgi?id=1091176>`__
..  [#ehpkp] `Under consideration <https://developer.microsoft.com/en-us/microsoft-edge/platform/status/publickeypinningextensionforhttp/>`__

..  [#cgapi] `In development <https://bugs.chromium.org/p/chromium/issues/detail?id=676016>`__
..  [#cnel] `In development <https://www.chromestatus.com/feature/5391249376804864>`__

..  [#enel] `Under consideration <https://developer.microsoft.com/en-us/microsoft-edge/platform/status/networkerrorlogging/>`__

..  [#cect] `Supported as of Chrome 61 <https://www.chromestatus.com/feature/5677171733430272>`__
..  [#fect] `Planned <https://lists.w3.org/Archives/Public/ietf-http-wg/2016OctDec/0767.html>`__
