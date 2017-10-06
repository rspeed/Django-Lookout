from logging import getLogger
from datetime import datetime
import json
import jsonschema


__all__ = ['ReportSchema', 'CSPSchema', 'HPKPSchema']

logger = getLogger(__name__)



class ReportSchema:
	@staticmethod
	def from_json (report_json):
		""" Factory to validate and instantiate reports based on their schema. """

		logger.debug("Decoding JSON")

		report = json.loads(report_json)

		logger.debug("Attempt to determine the type of report by testing each schema.")

		for schema in [ReportSchema, CSPSchema, HPKPSchema]:
			logger.debug("Trying {}".format(schema))

			if schema.is_valid(report):
				logger.debug("{} matched".format(schema))

				return schema(report, report_json)

		logger.error("No schemas matched!")


	@classmethod
	def is_valid (cls, report):
		try:
			jsonschema.validate(report, cls.SCHEMA)
		except jsonschema.ValidationError:
			return False
		else:
			return True


	def __init__(self, report, report_json):
		self.report = self.normalize(report)
		self.report_json = report_json


	# TODO Some form of template
	def __str__(self):
		return self.report_json


	SCHEMA = {
		"id": "",
		"$schema": "http://json-schema.org/draft-04/schema#",
		'title': 'HTTP Reporting API Reports',
		'description': "A collection of reports submitted by a user agent.",
		'type': 'array',
		'minItems': 1,
		'items': {
			'type': 'object',
			'required': ['type', 'age', 'url', 'body'],
			'properties': {
				'type': {
					'description': "The type of data the report contains.",
					'type': 'string'
				},
				'age': {
					'description': "The number of milliseconds between the report's timestamp and the current time.",
					'type': 'integer'
				},
				'url': {
					'description': "The URL of the page which triggered the report.",
					'type': 'string',
					'format': 'url'
				},
				'body': {
					'description': "The contents of the report as defined by the type.",
					'type': 'object'
				}
			}
		}
	}


	@staticmethod
	def normalize(report):
		return report



class CSPSchema (ReportSchema):
	SCHEMA = {
		'$schema': 'http://json-schema.org/draft-06/schema#',
		'title': 'Content Security Policy Report',
		'description': "A report sent by a user agent when a CSP is violated.",
		'type': 'object',
		'required': ['csp-report'],
		'properties': {
			'csp-report': {
				'type': 'object',
				'required': ['document-uri', 'blocked-uri', 'violated-directive'],
				'properties': {
					'document-uri': {
						'description': "The URL of the page which triggered the report.",
						'type': 'string',
						'format': 'url'
					},
					'original-policy': {
						'description': "The full policy that has been violated.",
						'type': 'string'
					},
					'violated-directive': {
						'description': "The policy directive that triggered the report.",
						'type': 'string'
					},
					'blocked-uri': {
						'description': "The URL of the resource which violated the policy.",
						'type': 'string',
						'format': 'url'
					},
					'referrer': {
						'description': "The referrer of the resource whose policy was violated.",
						'type': 'string',
						'format': 'url'
					},
					'disposition': {
						'description': "Whether the violation was enforced or just reported.",
						'type': 'string',
						'enum': ['enforce', 'report']
					}
				}
			}
		}
	}

	@staticmethod
	def normalize(report):
		report_body = report['csp-report']
		new_report = {
			'type': 'csp',
			'age': 0,  # CSP reports don't provide a date :\
			'url': report_body.pop('document-uri'),
			'body': report_body
		}
		return new_report



class HPKPSchema (ReportSchema):
	SCHEMA = {
		'$schema': 'http://json-schema.org/draft-06/schema#',
		'title': 'HTTP Public Key Pinning Report',
		'description': "A report sent by a user agent when a HPKP policy is violated.",
		'type': 'object',
		'required': ['date-time', 'hostname', 'known-pins'],
		'properties': {
			'date-time': {
				'description': "The time the user agent observed the pin validation failure.",
				'type': 'string',
				'format': 'date-time',
				'example': '2014-04-06T13:00:50Z'
			},
			'hostname': {
				'description': "The hostname to which the user agent made the original request that failed pin validation.",
				'type': 'string',
				'anyOf': [
					{'format': 'hostname'},
					{'format': 'ipv4'},
					{'format': 'ipv6'}
				],
				'example': 'www.example.com'
			},
			'port': {
				'description': "The port to which the user agent made the original request that failed pin validation.",
				'type': 'integer',
				'example': 443
			},
			'noted-hostname': {
				'description': "The hostname that the user agent noted when it noted the known pinned host.",
				'type': 'string',
				'anyOf': [
					{'format': 'hostname'},
					{'format': 'ipv4'},
					{'format': 'ipv6'}
				],
				'example': 'foo.example.com'
			},
			'include-subdomains': {
				'description': "Whether or not the user agent has noted the includeSubDomains directive for the known pinned host.",
				'type': 'boolean'
			},
			'served-certificate-chain': {
				'description': "The certificate chain, as served by the known pinned host during TLS session setup.",
				'type': 'array',
				'minItems': 1,
				'items': {
					'type': 'string'
				}
			},
			'validated-certificate-chain': {
				'description': "The certificate chain, as constructed by the user agent during certificate chain verification.",
				'type': 'array',
				'minItems': 1,
				'items': {
					'type': 'string'
				}
			},
			'known-pins': {
				'description': "The pins that the user agent has noted for the known pinned host.",
				'type': 'array',
				'items': {
					'type': 'string',
					'pattern': '^(.+)=(?:\'|")(.+)(?:\'|")$'
				}
			},
			'effective-expiration-date': {
				'description': "The effective expiration date for the noted pins.",
				'type': 'string',
				'format': 'date-time',
				'example': '2014-05-01T12:40:50Z'
			}
		}
	}


	@staticmethod
	def normalize (report):
		""" Normalize HPKP schema to HTTP Reporting API schema """

		new_report = {
			'type': 'hpkp',
			'age': datetime.now() - report.pop('date-time'),
			'url': 'https://{}/'.format(report.pop('hostname')),
			'body': report
		}
		return new_report

