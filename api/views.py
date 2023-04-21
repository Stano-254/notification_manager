from api.backend.notification_processor import Processor
from django.core.files.storage import FileSystemStorage
from api.backend.utils import get_client_ip
from django.http import JsonResponse
from django.conf import settings
import logging

lgr = logging.getLogger(__name__)


def send_message(request):
	try:
		request_data = request.POST.copy()
		source_ip = get_client_ip(request)
		files = None
		if request_data("attached", False):
			fs_path = settings.TEMP_CONTENT_ROOT
			files = []
			count = 1
			for file in request.FILES:
				print(f"file no {count}, file {file.name}")
				fs = FileSystemStorage(fs_path)
				fs.save(file.name, file)
				files.append(fs_path + file.name)
				count += 1

		return JsonResponse(Processor().send_message(
			destination=request_data.get('destination', None), type_code=request_data.get('message_type', None),
			request=request_data, replace_tags=request_data.get('replace_tags', None), source_ip=source_ip,
			app_code=request.get('app_code', None), message_code=request_data.get('message_code', None),
			lang=request_data.get('lang', None), attachment=files, cc=request_data.get("cc", None),
			corporate_id=request_data.get('corporate_id', request_data.get('organization_id', '')),
			subject=request_data.get('subject', None)
		))

	except Exception as e:
		lgr.exception(f"error during send message:{e}")
