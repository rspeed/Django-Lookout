from logging import getLogger
import json
import jsonschema

from django.utils import timezone

from .exceptions import UnknownSchemaError


__all__ = ['ReportSchema', 'CSPSchema', 'HPKPSchema']

logger = getLogger(__name__)



class BaseSchema:

	@property
	def SCHEMA (self):
		""" A dictionary representing the JSON schema of a certain type of incident report. """
		return NotImplementedError()

	data = {}

	# Caches a JSON-serialized version of the report data.
	# It should only be access by casting the object to a string.
	_serialized = None


	@classmethod
	def from_json (cls, report_json):
		""" Factory to instantiate incident report objects based on their schema. """

		logger.debug("Decoding JSON")
		report_datum = json.loads(report_json)

		# Wrap single reports in a list
		if not isinstance(report_datum, list):
			report_datum = [report_datum]

		for report_data in report_datum:
			logger.debug("Attempt to determine the type of report by testing each schema.")

			yield cls.get_matching_schema(report_data)


	@staticmethod
	def get_matching_schema (report_data):
		""" Returns a BaseSchema-subclassed object containing the report_data. """
		for schema in [ReportSchema, CSPSchema, HPKPSchema]:
			logger.debug("Trying {}".format(schema))

			if schema.is_valid(report_data):
				logger.debug("Validated as {}".format(schema))

				# Create the schema object
				return schema(report_data)

		logger.warning("No schemas matched!")
		raise UnknownSchemaError()


	@classmethod
	def is_valid (cls, report_data):
		""" Checks to see if the report data matches the schema. """
		try:
			jsonschema.validate(report_data, cls.SCHEMA)
		except jsonschema.ValidationError:
			return False
		else:
			return True


	@staticmethod
	def normalize(report_data):
		""" Used by subclasses to adapt legacy schemas. """

		return report_data


	def __init__(self, report_data):
		self.data = self.normalize(report_data)


	# TODO Some form of template
	def __str__(self):
		# Re-serialize the data
		if self._serialized is None:
			self._serialized = json.dumps(self.data)

		return self._serialized


	def __iter__ (self):
		""" Allows the object to be iterated and (more importantly) cast to a dict. """

		return iter(self.data.items())



class ReportSchema (BaseSchema):
	""" Represents a HTTP Reporting API incident report bound to a definition of its schema. """

	# TODO Add definitions and dependencies for each type/body combination.
	SCHEMA = {
		'$schema': "http://json-schema.org/draft-04/schema#",
		'title': "HTTP Reporting API incident report",
		'description': "An incident report submitted by a user agent.",
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



class CSPSchema (BaseSchema):
	"""
	Represents a legacy Content Security Policy incident report bound to a definition of its schema.
	Wrapped in a base HTTP Reporting API incident schema.
	"""

	SCHEMA = {
		'$schema': 'http://json-schema.org/draft-04/schema#',
		'title': 'Content Security Policy Report',
		'description': "An incident report sent by a user agent when a CSP is violated.",
		'type': 'object',
		'required': ['csp-report'],
		'additionalProperties': False,
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
	def normalize (report_data):
		""" Adapts the legacy CSP schema. """

		report_data = report_data['csp-report']

		return {
			'type': 'csp',
			'age': 0,  # CSP reports don't provide a date :\
			'url': report_data.pop('document-uri'),
			'body': report_data
		}



class HPKPSchema (BaseSchema):
	SCHEMA = {
		'$schema': 'http://json-schema.org/draft-04/schema#',
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
	def normalize (report_data):
		""" Adapts the legacy HPKP schema to the HTTP Reporting API schema """

		return {
			'type': 'hpkp',
			'age': timezone.now() - report_data.pop('date-time'),
			'url': 'https://{}/'.format(report_data.pop('hostname')),
			'body': report_data
		}

