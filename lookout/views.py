import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.template.loader import get_template
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from .models import Report
from .logging import ReportMessage
from .exceptions import JSONDecodeError, UnknownSchemaError


__all__ = ['ReportView']


logger = logging.getLogger('lookout')



@method_decorator(csrf_exempt, name='dispatch')
class ReportView (View):
	""" Logs the report and returns an empty response. """

	http_method_names = ['post']


	@staticmethod
	def post(request):
		""" Handles the POST request. """

		try:
			reports = Report.objects.create_from_json(request.body.decode('utf8'))

			# Log the reports
			for report in reports:
				logger.error(ReportMessage(report=report))

		except JSONDecodeError:
			return HttpResponseBadRequest("Request body was not valid JSON.")

		except UnknownSchemaError:
			return HttpResponseBadRequest("Request body didn't match any known schema.")

		# Return an empty HTTP 200
		return HttpResponse('')
