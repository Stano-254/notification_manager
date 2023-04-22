import calendar

from api.backend.notification_processor import Processor
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from api.backend.utils import get_client_ip, __error_400, __response, __success, __error_500
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.conf import settings
import logging

from api.decorators import authentication_wrapper
from api.oauth import OAuth
from core.backend.services import AppService

lgr = logging.getLogger(__name__)


@authentication_wrapper
@csrf_exempt
def send_message(request):
	try:
		request_data = request.POST.copy()
		source_ip = get_client_ip(request)
		files = None
		if request_data.get("attached", False):
			fs_path = settings.TEMP_CONTENT_ROOT
			files = []
			count = 1
			for file in request.FILES:
				file = request.FILES[file]
				print(f"file no {count}, file {file.name}")
				fs = FileSystemStorage(fs_path)
				fs.save(file.name, file)
				files.append(fs_path + file.name)
				count += 1

		return JsonResponse(Processor().send_message(
			destination=request_data.get('destination', None), type_code=request_data.get('message_type', None),
			request=request_data, message_data=request_data.get('message_data', None), source_ip=source_ip,
			app_code=request_data.get('app_code', None), message_code=request_data.get('message_code', None),
			lang=request_data.get('lang', None), attachment=files, cc=request_data.get("cc", None),
			corporate_id=request_data.get('corporate_id', request_data.get('organization_id', '')),
			subject=request_data.get('subject', None)
		))

	except Exception as e:
		lgr.exception(f"error during send message:{e}")

@csrf_exempt
def get_access_token(request):
	"""
	get user access token
	:param request:
	:return:
	"""
	try:
		if request.method == "POST":
			username = request.POST.get('username', None)
			client_secret = request.POST.get('client_secret', None)
			client_id = request.POST.get('client_id', None)
			app = AppService().get(id=client_id, state__name="Active")
			data = None
			if app:
				user = authenticate(username=username, password=client_secret)
				if user:
					auth = OAuth().generate_account_token(access_app=app, user=user)
					if auth:
						try:
							auth = OAuth().get_valid_account_access_token(user)
							if not auth:
								raise Exception
							data = {
								'token': str(auth.access_token),
								'expires': str(calendar.timegm(auth.expires_at.timetuple()))
							}
							print(data)
						except Exception as e:
							lgr.error(f'login Exception {e}')
							return __error_400(__response("failed", "invalid login attempt"))
			return __success(__response("success", "Successfully logged in user.", data))
		return __error_400(__response('failed', 'Invalid login attempt'))

	except Exception as e:
		lgr.error(f'login Exception:{e}')
	return __error_500(__response('failed', 'wrong request'))
