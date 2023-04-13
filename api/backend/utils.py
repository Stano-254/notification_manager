import json
from django.http import HttpResponse, JsonResponse


def get_client_ip(request):
	x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
	if x_forwarded_for:
		ip = x_forwarded_for.split(',')[0]
	else:
		ip = request.META.get('REMOTE_ADDR')
	return ip


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
