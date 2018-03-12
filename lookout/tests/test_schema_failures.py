from django.test import TestCase

from lookout.report_schemas.base import ReportSchema
from lookout.report_schemas.generic import GenericReportSchema



class TestReportSchemaNotImplemented (TestCase):
	""" Tests that schemas based on ``ReportSchema`` implement all of its abstract methods. """

	def test_schema (self):
		try:
			class BadSchema (ReportSchema):
				type = 'empty'
				name = 'empty'
				description = "empty"

			BadSchema.schema
		except NotImplementedError:
			pass
		else:
			self.fail("BadSchema.schema should have raised a NotImplementedError")


	def test_type (self):
		try:
			class BadSchema (ReportSchema):
				schema = 'empty'
				name = 'empty'
				description = "empty"

			BadSchema.type
		except NotImplementedError:
			pass
		else:
			self.fail("BadSchema.type should have raised a NotImplementedError")


	def test_name (self):
		try:
			class BadSchema (ReportSchema):
				schema = 'empty'
				type = 'empty'
				description = "empty"

			BadSchema.name
		except NotImplementedError:
			pass
		else:
			self.fail("BadSchema.name should have raised a NotImplementedError")


	def test_description (self):
		try:
			class BadSchema (ReportSchema):
				schema = 'empty'
				type = 'empty'
				name = 'empty'

			BadSchema.description
		except NotImplementedError:
			pass
		else:
			self.fail("BadSchema.description should have raised a NotImplementedError")



class TestGenericReportSchemaNotImplemented (TestCase):
	""" Tests that schemas based on ``GenericReportSchema`` implement all of its abstract methods. """

	def test_body_schema (self):
		try:
			class BadSchema (GenericReportSchema):
				type = 'empty'
				name = 'empty'
				description = "empty"

			BadSchema.body_schema
		except NotImplementedError:
			pass
		else:
			self.fail("BadSchema.body_schema should have raised a NotImplementedError")
