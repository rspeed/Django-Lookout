import logging

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .logging import ReportMessage
from .schemas import ReportSchema


__all__ = ['ReportView']


logger = logging.getLogger('http_reporting_api')



@method_decorator(csrf_exempt, name='dispatch')
class ReportView (View):
	""" Logs the report and returns an empty response. """

	http_method_names = ['post']


	def post(self, request):
		""" Handles the POST request. """

		try:
			report = ReportSchema.from_json(request.body.decode('utf8'))
		except Exception as e:
			# TODO Implement custom exceptions
			return HttpResponseBadRequest("Request body was not valid JSON.")

		# Log the report
		logger.error(ReportMessage(report=report))

		# Return an empty HTTP 200
		return HttpResponse('')
