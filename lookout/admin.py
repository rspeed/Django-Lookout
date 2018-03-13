import typing

from django.contrib import admin
from django.http import HttpRequest

from .models import Report



@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
	date_hierarchy = 'created_time'

	empty_value_display = '<i>[empty]</i>'

	list_display = ['created_time', 'type']
	list_filter = ['created_time', 'incident_time', 'type']

	save_on_top = True
	actions = None

	fieldsets = [
		[None, {
			'fields': ['created_time', 'incident_time', 'type', 'url']
		}],
		["Details", {
			'description': "The report's full contents.",
			'fields': ['pretty_body'],
		}]
	]


	def get_readonly_fields (self, request: HttpRequest, obj=None) -> typing.List[str]:
		""" Marks all fields as read-only. """
		# Don't use self.get_fields, as that causes an infinite recursion
		fields = self.fields or []
		for fieldset in self.fieldsets or []:
			fields.extend(fieldset[1].get('fields', []))
		return fields


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
