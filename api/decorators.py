"""
helper functions for API endpoint
"""
import json
from functools import wraps
from django.utils import timezone
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse
from core.backend.services import OAuthService


def authentication_wrapper(view_func):
	"""
	check if the request is from API then ensure user has been set
	otherwise call the login required
	:param view_func:
	:return:
	"""

	def view_wrapper(*args, **kwargs):
		is_checked = False
		for k in args:
			if isinstance(k, WSGIRequest):
				if (k.POST.get('client_id', False) or k.GET.get('client_id', False)) and (
						k.POST.get('token', False) or k.GET.get('token', False)):
					if k.method == "POST":
						token = k.POST.get('token')
						client_id = k.POST.get('client_id')
					else:
						token = k.GET.get('token')
						client_id = k.GET.get('client_id')
					oauth = OAuthService().filter(
						access_token=str(token), app__id=str(client_id), expires_at__gt=timezone.now()).exists()
					is_checked = True
					if not oauth:
						response = HttpResponse(
							json.dumps({
								'status': 'failed', 'message': 'Unauthorized'}),
							content_type='application/json', status=401
						)
						response['WWW-Authenticate'] = 'Bearer realm=api'
				else:
					return HttpResponse(
						json.dumps({'status': 'failed', 'message': 'Unauthorized'}),
						content_type='application/json', status=401)
		if not is_checked:
			response = HttpResponse(
				json.dumps({'status': 'failed', 'message': 'Unauthorized'}),
				content_type='application/json', status=401)
			response['WWW-Authenticate'] = 'Bearer realm=api'
			return response
		return view_func(*args, **kwargs)
	return wraps(view_func)(view_wrapper)
