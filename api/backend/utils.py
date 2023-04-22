import base64
import binascii
import json
import os
import re
from decimal import Decimal
from datetime import datetime, date, timedelta
from django.http import HttpResponse, JsonResponse
from django.conf import settings
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


def clean_phone_number(phone, total_count = 12, country_code = None):
	"""
	Normalizes and cleans a phone number, ensuring that it has a valid country code and the required count
	@param phone: The phone number to normalize
	@type phone: str
	@param total_count: The total digits required
	@type total_count: int
	@param country_code: The country code for the phone
	@type country_code: str | None
	@return: a normalized phone number
	@rtype: str
	"""
	if country_code is None:
		country_code = settings.DEFAULT_COUNTRY_CODE

	if str(phone).startswith('+'):
		phone = str(phone)[1:]
	if len(phone) == total_count:
		return phone
	elif (len(phone) + len(country_code)) == total_count:
		return str(country_code) + str(phone)
	elif str(phone).startswith('0') and ((len(phone) - 1) + len(country_code)) == total_count:
		return str(country_code) + str(phone)[1:]
	else:
		if len(country_code) > 0:
			overlap = abs((len(phone) + len(country_code)) - total_count)
			return str(country_code) + str(phone)[overlap - 1:]
		else:
			return phone


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


def json_super_serializer(obj):
	"""
	Automatic serializer for objects not serializable by default by the JSON serializer.
	Includes datetime, date, Decimal
	@param obj: The object to convert.
	@return: String of the data converted.
	@rtype: str
	"""
	if isinstance(obj, datetime):
		# noinspection PyBroadException
		try:
			return obj.strftime('%d/%m/%Y %I:%M:%S %p')
		except Exception:
			return str(obj)
	elif isinstance(obj, date):
		# noinspection PyBroadException
		try:
			return obj.strftime('%d/%m/%Y')
		except Exception:
			return str(obj)
	elif isinstance(obj, (Decimal, float)):
		return str("{:,}".format(round(Decimal(obj), 2)))
	elif isinstance(obj, timedelta):
		return obj.days
	return str(obj)


def generate_token():
	"""
	Generates a standard token to be used for ABC + etc.
	@return: The string representation of token 20 characters.
	@rtype: str | None
	"""
	try:
		return base64.b64encode(binascii.hexlify(os.urandom(15))).decode()
	except Exception as e:
		lgr.exception('generate_token Exception: %s', e)
	return None


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


def call_class_method(self, class_instance, function_name, **kwargs):
	"""
	Calls the given method on the class instance provided passing in the kwargs
	@param class_instance: The instance of the class to call a function in.
	@type class_instance: object
	@param function_name: The function name to call on the class.
	@type function_name: str
	@param kwargs: The arguments to pass to the class method.
	@return: The results of processing the function on the class.
	@rtype: object
	"""
	try:
		return getattr(class_instance, function_name)(**kwargs)
	except Exception as e:
		lgr.exception('%s call_class_method Exception: %s', self.__class__.__name__, e)
	return None

