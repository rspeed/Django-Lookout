from logging import getLogger
from collections import OrderedDict
import jsonschema

from ..utils import attribute
from ..exceptions import UnknownSchemaError


__all__ = ['report_schema_registry', 'get_matching_schema', 'ReportSchema']


logger = getLogger(__name__)

report_schema_registry = OrderedDict()



def get_matching_schema (report_data):
	""" Returns the first ``ReportSchema`` class which validates the report data. """

	for name, schema in report_schema_registry.items():
		logger.debug("Trying {}".format(name))

		if schema.is_valid(report_data):
			logger.debug("Validated as {}".format(name))

			return schema

	logger.warning("No schemas matched!")
	raise UnknownSchemaError()



class ReportSchemaBase (type):
	""" Base metaclass which adds ``ReportSchema``s to the registry. """

	def __new__(mcs, name, bases, attributes):

		# Create the class object
		new_class = super().__new__(mcs, name, bases, attributes)

		try:
			abstract = attributes['Meta'].abstract
		except (AttributeError, KeyError):
			# The Meta object or abstract property aren't set
			abstract = False

		# Add non-abstract classes to the registry
		if not abstract:
			report_schema_registry[new_class.type] = new_class

		return new_class



class ReportSchema (metaclass=ReportSchemaBase):

	class Meta:
		abstract = True


	@attribute
	@classmethod
	def schema (cls):
		""" A dictionary representing the JSON schema of a certain type of incident report. """
		return NotImplementedError


	@attribute
	@classmethod
	def type (cls):
		return NotImplementedError


	@attribute
	@classmethod
	def name (cls):
		return NotImplementedError


	@attribute
	@classmethod
	def description (cls):
		return NotImplementedError


	@classmethod
	def is_valid (cls, report_data):
		""" Checks to see if the report data matches the schema. """

		try:
			jsonschema.validate(report_data, cls.schema)
		except jsonschema.ValidationError:
			return False
		else:
			return True


	@classmethod
	def normalize(cls, report_data):
		""" Converts legacy schemas to their generic equivalent. """

		return cls, report_data
