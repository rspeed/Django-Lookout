import re

from django.contrib import admin

from .models import Report



def camel_to_label (camel_input):
	""" Converts a camel-case string into a space-delimited label. """

	# Handles capitalization logic
	def capitalization (word, index):
		# Keep acronyms upper-case
		if word.isupper():
			return word
		# Capitalize the first word
		if index == 0:
			return word.capitalize()
		# Everything else is lower-case
		return word.lower()

	# Split the input into individual words, acronyms, and numbers
	words = re.findall(r'[A-Z]?[a-z]+|[A-Z]{2,}(?=[A-Z][a-z]|\d|\W|$)|\d+', camel_input)

	# Convert (most) words to lower case, then join them with spaces
	return ' '.join([capitalization(word, i) for i, word in enumerate(words)])



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	date_hierarchy = 'created'

	empty_value_display = '<i>[empty]</i>'

	list_display = ['created', 'type']
	list_filter = ['created', 'type', 'generated']

	save_on_top = True
	actions = None

	fieldsets = [
		[None, {
			'fields': ['created', 'generated', 'url']
		}],
		["Body", {
			'description': "The report's full contents.",
			'fields': ['pretty_body'],
		}]
	]


	def get_readonly_fields (self, request, obj=None):
		""" Marks all fields as read-only. """
		fields = self.fields or [f.name for f in self.model._meta.fields]
		return fields + ['pretty_body']


	def has_add_permission (self, request):
		""" Disables the ability to add reports through the admin. """
		return False


	def has_change_permission (self, request, obj=None):
		""" Disables the ability to edit reports through the admin. """

		# Normal permissions are granted when viewing the form, or else it would display an error
		return request.method in ['GET', 'HEAD'] and super().has_change_permission(request, obj)


	def has_delete_permission(self, request, obj=None):
		""" Disables the ability to delete reports through the admin. """
		return False
