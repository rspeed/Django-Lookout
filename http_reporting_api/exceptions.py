from json import JSONDecodeError  # Inherit so it can be imported from this module


__all__ = ['UnknownSchemaError', 'JSONDecodeError']



class UnknownSchemaError (Exception):
	""" Raised when a report doesn't match any of the known schemas. """

	msg = "The supplied JSON data doesn't match any known report schema."
