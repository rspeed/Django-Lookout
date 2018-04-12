from datetime import timedelta, datetime

from django.utils import timezone, dateparse

from .generic import GenericReportSchema
from .legacy import LegacyReportSchema


__all__ = ['HPKPReportSchema', 'LegacyHPKPReportSchema']



class HPKPReportSchema (GenericReportSchema):
	type = 'hpkp'
	name = "HTTP Public Key Pinning Report"
	description = "A report sent by a user agent when a HPKP policy is violated."


	body_schema = {
		'required': ['hostname'],
		'properties': {
			'hostname': {
				'description': "The hostname to which the user agent made the original request that failed pin validation.",
				'type': 'string',
				'anyOf': [
					{'format': 'hostname'},
					{'format': 'ipv4'},
					{'format': 'ipv6'}
				]
			},
			'port': {
				'description': "The port to which the user agent made the original request that failed pin validation.",
				'type': 'integer'
			},
			'noted-hostname': {
				'description': "The hostname that the user agent noted when it noted the known pinned host.",
				'type': 'string',
				'anyOf': [
					{'format': 'hostname'},
					{'format': 'ipv4'},
					{'format': 'ipv6'}
				]
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
				'format': 'date-time'
			}
		}
	}



class LegacyHPKPReportSchema (LegacyReportSchema):

	generic_class = HPKPReportSchema


	def normalize (self, report_data):
		""" Adapts the legacy HPKP schema to the HTTP Reporting API schema """
		now = datetime.now(timezone.utc)
		report_datetime = dateparse.parse_datetime(report_data.pop('date-time'))

		# Make sure ``report_datetime`` is timezone-aware
		if timezone.is_naive(report_datetime):
			# Assume UTC, since we can't reliably know where the client is located
			report_datetime = timezone.make_aware(report_datetime, timezone.utc)

		# The number of milliseconds between ``date-time`` and now
		age = (now - report_datetime) / timedelta(milliseconds=1)

		return self.generic_class, {
			'type': self.type,
			'age': age,
			'url': 'https://{}/'.format(report_data.get('hostname', '')),
			'body': report_data
		}
