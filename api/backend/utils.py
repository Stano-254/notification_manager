import json
import re
from datetime import datetime
from django.http import HttpResponse, JsonResponse
import uuid
import logging

lgr = logging.getLogger(__name__)


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


def generate_confirmation_key():
	"""
	function generates confirmation code
	:return: generated confirmation code SY-20234567899_4485599dfng
	:rtype:str
	"""
	uid = str(uuid.uuid4()).replace('-', '')
	return f"SY-{datetime.now().strftime('%Y%m%d%H%M%S')}_{uid[:14]}"


def validate_email(email):
	"""
	check if email provide is a valid email
	:param email:
	:return: True is valid False otherwise
	"""
	try:
		if re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
			return True
	except Exception as e:
		lgr.error(f'validate_email : {e}')
	return False


def __error_403(response):
	return JsonResponse(response, content_type='application/json', status=403, safe=False)


def __error_400(response):
	return JsonResponse(response, safe=False, status=400)


def __error_500(response):
	return JsonResponse(response, safe=False, status=500)


def __success(response):
	return JsonResponse(response, safe=False, status=200)


def __response(status, message, data=None):
	return {'status': status, 'message': message, "data": data}
