from collections import Mapping

from django.apps import AppConfig
from django.conf import settings as project_settings
from django.core.exceptions import ImproperlyConfigured
from django.core.checks import Warning, register as register_check



class DjangoLookoutConfig(AppConfig):
	""" AppConfig with settings that can be overridden in settings.py. """

	name = 'lookout'
	verbose_name = "Django Lookout"


	SAVE_REPORTS = True
	""" Whether the Django-Lookout should always save new reports as ``lookout.models.Report`` instances. """


	def ready (self):
		""" Updates the AppConfig with values from the project settings. """

		checks = []

		# Look for a settings dictionary
		try:
			settings = getattr(project_settings, self.name.upper())
			assert(isinstance(settings, Mapping))

		except AssertionError:
			raise ImproperlyConfigured("The {0!r} setting must be a dictionary-like object.".format(self.name.upper()))

		except AttributeError:
			# No settings dictionary
			pass

		else:
			# Update the AppConfig
			for key, value in settings.items():
				try:
					# Validate the key
					assert(key.isupper())
					assert(hasattr(self, key))

					setattr(self, key, value)

				except AssertionError:
					checks.append(Warning(
						"{0!r} is not a valid setting name for {1}.".format(key, self.verbose_name),
						hint="The key must be all-caps and have an equivalent default setting.",
						obj=settings
					))

		@register_check
		def show_checks (app_configs, **kwargs):
			return checks
