Django Lookout
==============

[![Build Status](https://travis-ci.org/rspeed/Django-Lookout.svg?branch=master)](https://travis-ci.org/rspeed/Django-Lookout)

![Django Lookout logo: a lookout tower](./lookout/docs/logo.svg)

A Django-based API endpoint for collecting and processing automatic incident reports send by your visitors' web browsers. Currently that includes both [Content Security Policy](https://en.wikipedia.org/wiki/Content_Security_Policy) (CSP) and [HTTP Public Key Pinning](https://en.wikipedia.org/wiki/HTTP_Public_Key_Pinning) (HPKP), but support for additional report types is planned.

Before getting started you should familiarize yourself with the standards and their potential pitfalls ([especially HPKP](https://www.smashingmagazine.com/be-afraid-of-public-key-pinning/)). The risks can be mitigated significantly by using Django Lookout along with report-only policies, which would still allow you to be notified of potential attacks without the risk of accidentally rendering your web site inaccessible.

It's important to note that Django Lookout only handles the *reporting* part of the process. Setting the headers which tell browsers what to do, or even where to send reports, is outside its scope. You'll need to set the `report-uri` property for CSP and/or HPKP to point to your Django Lookout endpoint.


## Install and Configure

**Notes**

* If you're using HPKP, Django Lookout *has* to be set up on a different domain name.


### Step 1

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


### Step 2

Add the API endpoint to `urls.py`.

```python
urlpatterns = [
	...
	# Django Lookout
	url(r'^reporting', include('lookout.urls')),
	...
]
```

**Notes**

* You can set the pattern to whatever you want. That's where you'll be pointing `report-uri`.
* Be mindful of trailing slashes.


### Step 3

Run the database migrations:

```bash
./manage.py migrate lookout
```


## Useful Guides

### Content Security Policy

* [Google Web Fundamentals – Content Security Policy](https://developers.google.com/web/fundamentals/security/csp/)
* [Content Security Policy - An Introduction](https://scotthelme.co.uk/content-security-policy-an-introduction/)

### HTTP Public Key Pinning

* [Google – Rolling out Public Key Pinning with HPKP Reporting](https://developers.google.com/web/updates/2015/09/HPKP-reporting-with-chrome-46)
* [Guidance on setting up HPKP](https://scotthelme.co.uk/guidance-on-setting-up-hpkp/)


## Standards

Support for these standards is planned to be implemented in Django Lookout 1.0.

- [Out-of-Band Reporting API](https://wicg.github.io/reporting/) ✅  
  A generic incident reporting API that can be used by all of the following standards. Django Lookout automatically converts "legacy" incident reports to the generic schema.
- [Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP) ✅  
  Browsers will (optionally) block unauthorized content and send an incident report if a resource is requested which isn't permitted by the policy.
- [HTTP Public Key Pinning](https://developer.mozilla.org/en-US/docs/Web/HTTP/Public_Key_Pinning) ✅  
  Browsers supporting HPKP will (optionally) block connections and send an incident report if the site doesn't use the specified HTTPS certificate in the future.
- [Network Error Logging](http://wicg.github.io/network-error-logging/)  
  Browsers supporting NEL will send incident reports if a networking error is encountered when requesting content.
- [Expect-CT](https://tools.ietf.org/html/draft-ietf-httpbis-expect-ct-02)  
  Browsers supporting Report-CT will send an incident report if it receives a certificate which doesn't adhere to [Certificate Transparency](https://www.certificate-transparency.org/) guidelines.
- [Expect-Staple](https://scotthelme.co.uk/ocsp-expect-staple/)  
  Browsers supporting Expect-Staple will send an incident report if a TLS handshake with the site doesn't include an [OCSP response](https://en.wikipedia.org/wiki/OCSP_stapling).


### Browser Implementation Status

No standards are currently supported across all major browsers, though it's hoped that the generic reporting API will significantly improve the situation in modern browsers.


**Notes**

* This table only considers a feature supported if it includes reporting functionality.
* Internet Explorer is excluded due to the fact that it doesn't support any of these features via standard headers.

|                                     | Chrome         | Edge                      | Firefox                  | Safari         |
| ----------------------------------: | :------------- | :------------------------ | :----------------------- | :------------- |
| **Content Security Policy (CSP)**   | Supported      | [Supported][2]            | Supported                | [Supported][4] |
| **HTTP Public Key Pinning (HPKP)**  | [Supported][5] | [Under Consideration][6]  | [Not Supported][7]       | Not Supported  |
| **Out-of-Band Reporting API**       | [Planned][9]   | Not Supported             | Not Supported            | Not Supported  |
| **Network Error Logging (NEL)**     | [Planned][13]  | [Under Consideration][14] | Not Supported            | Not Supported  |
| **Expect-CT**                       | [Planned][17]  | [Planned][18]             | ?                        | ?              |
| **Expect-Staple**                   | ?              | ?                         | ?                        | ?              |


[2]: https://developer.microsoft.com/en-us/microsoft-edge/platform/status/contentsecuritypolicylevel2/ "Partial support for Level 3"
[4]: https://webkit.org/status/#specification-content-security-policy-level-3 "Partial support for Level 3"

[5]: https://www.chromestatus.com/feature/4669935557017600
[6]: https://developer.microsoft.com/en-us/microsoft-edge/platform/status/publickeypinningextensionforhttp/ "Under Consideration"
[7]: https://bugzilla.mozilla.org/show_bug.cgi?id=1091176 "No report-uri or report-only support."

[9]: https://bugs.chromium.org/p/chromium/issues/detail?id=676016

[13]: https://www.chromestatus.com/feature/5391249376804864 "No recent progress"
[14]: https://developer.microsoft.com/en-us/microsoft-edge/platform/status/networkerrorlogging/

[17]: https://bugs.chromium.org/p/chromium/issues/detail?id=679012
[18]: https://lists.w3.org/Archives/Public/ietf-http-wg/2016OctDec/0767.html


## Tools and Similar Projects

* [Observatory by Mozilla](https://observatory.mozilla.org/). General website security testing suite.
* [securityheaders.io](https://securityheaders.io). Testing suite for security-related HTTP response headers.
* [django-csp-reports](https://github.com/adamalton/django-csp-reports). A similar project specifically for CSP reports.
* [report-uri.io](https://report-uri.io/). A commercial service which serves a similar purpose. They also have some useful free testing tools.
