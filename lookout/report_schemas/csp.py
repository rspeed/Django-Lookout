from .generic import GenericReportSchema
from .legacy import LegacyReportSchema


__all__ = ['CSPReportSchema', 'LegacyCSPReportSchema']



class CSPReportSchema (GenericReportSchema):
	type = 'csp'
	name = "Content Security Policy Report"
	description = "An incident report sent by a user agent when a CSP is violated."

	body_schema = {
		'type': 'object',
		'required': ['blocked', 'directive'],
		'properties': {
			'policy': {
				'description': "The full policy that has been violated.",
				'type': 'string'
			},
			'directive': {
				'description': "The policy directive that triggered the report.",
				'type': 'string'
			},
			'blocked': {
				'description': "The URL of the resource which violated the policy.",
				'type': 'string',
				'format': 'url'
			},
			'referrer': {
				'description': "The referrer of the resource whose policy was violated.",
				'type': 'string',
				'format': 'url'
			},
			'status-code': {
				'description': "The HTTP status code of the request which triggered the report.",
				'type': 'integer'
			},
			'disposition': {
				'description': "Whether the violation was enforced or just reported.",
				'type': 'string',
				'enum': ['enforce', 'report']
			},
			'source-file': {
				'type': 'string',
				'description': "The URL of the resource where action which triggered the violation initiated."
			},
			'line-number': {
				'type': 'number',
				'description': "The line number in source-file on which the violation occurred."
			},
			'column-number': {
				'type': 'number',
				'description': "The column number in source-file on which the violation occurred."
			}
		}
	}



class LegacyCSPReportSchema (LegacyReportSchema):
	"""
	Represents a legacy Content Security Policy incident report bound to a definition of its schema.
	Wrapped in a base HTTP Reporting API incident schema.
	"""

	generic_class = CSPReportSchema
	root_object_name = 'csp-report'


	body_schema = {
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
			'effective-directive': {
				'type': 'string',
				'description': "The policy directive that was violated. Generally equivalent to `violated-directive`."
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
			'status-code': {
				'description': "The HTTP status code of the request which triggered the report.",
				'type': 'integer'
			},
			'disposition': {
				'description': "Whether the violation was enforced or just reported.",
				'type': 'string',
				'enum': ['enforce', 'report']
			},
			'source-file': {
				'type': 'string',
				'description': "The URL of the resource where action which triggered the violation initiated."
			},
			'line-number': {
				'type': 'number',
				'description': "The line number in source-file on which the violation occurred."
			},
			'column-number': {
				'type': 'number',
				'description': "The column number in source-file on which the violation occurred."
			}
		}
	}


	@classmethod
	def normalize (cls, report_data):
		""" Adapts the legacy CSP schema. """

		report_data = report_data[cls.root_object_name]

		# Remap keys
		remap = {
			'blocked-uri': 'blocked',
			'violated-directive': 'directive',
			'effective-directive': 'directive',
			'original-policy': 'policy'
		}
		for from_key, to_key in remap.items():
			if to_key not in report_data:
				value = report_data.pop(from_key, None)
				if value is not None:
					report_data[to_key] = value

		return cls.generic_class, {
			'type': cls.generic_class.type,
			'age': 0,  # CSP reports don't provide a date :\
			'url': report_data.pop('document-uri'),
			'body': report_data
		}
