import json
import time
import traceback
from datetime import datetime

from django.utils import timezone
import requests

from api.backend.utils import json_super_serializer


def send_notification(notifications):
	"""
	Sends notifications through the Notifications Bus. The notifications are passed in as a list of dictionaries
	which it then evaluates and makes the http calls
	@param notifications: list of dictionaries for notifications to be sent
	@type notifications: list
	@param trans: The transaction that the notifications are sent against
	@type trans: Transaction Model object
	@return: None
	@rtype: None
	"""
	try:
		if not notifications:
			return None
		# if not settings.SEND_NOTIFICATIONS:
		# 	return 'success'
		# CLIENT_ID: 'c46eb507-747f-4a0a-8436-ebca221f2e0d'
		# CLIENT_SECRET: 'Crunch321#'
		# BUS_USERNAME: 'radicrunch'
		# BUS_URL: 'https://bus.spinmobile.co'
		# APP_CODE: '004'
		access_token_data = {
			'username': 'ecommerce',  #settings.BUS_USERNAME,
			'client_id': '5369a2c6-bd9f-4d90-9575-bc0bab87b1c5', #settings.CLIENT_ID,
			'client_secret': 'Cosmic3421$#' #settings.CLIENT_SECRET
		}
		files = ""
		for notification in notifications:
			# lgr.info("on boarding notification", notification)
			if notification['message_type'] == '1':
				notification_name = 'SMS'
			elif notification['message_type'] == '2':
				notification_name = 'EMAIL'
			else:
				notification_name = 'SYS'
			# notification_type = NotificationTypeService().get(name=notification_name)
			# organization = OrganizationService().get(id=notification.get('organization_id', ''))
			# message = json.dumps(notification.get('replace_tags', ''), default=json_super_serializer)
			files = notification.get('files', None)
			# destination = notification.get('destination', '')
			# noti = NotificationService().create(
			# 	notification_type=notification_type, organization=organization,
			# 	title=notification.get('message_code', ''), message=message,
			# 	destination=destination, state=StateService().get(name='Sent'))
			# if not noti:
			# 	return 'Notifications Down'
			if notification_name != 'SYS':
				res = requests.post(url='%s/api/%s/' % ('https://5fea-105-163-157-75.ngrok-free.app', 'get_access_token'), data=access_token_data, verify=False, timeout=None).text
				print(res)
				resp = json.loads(res)
				access_token = resp.get('data', {}).get('token', None)
				if access_token is None:
					time.sleep(20)
					resps = requests.post(
							url='%s/api/%s/' % ('https://5fea-105-163-157-75.ngrok-free.app', 'get_access_token'),
							data=access_token_data, verify=False, timeout=None).text
					print(resps)
					resp = json.loads(resps)
					access_token = resp.get('data', {}).get('token', '')
				if access_token is None:
					continue
				notification['token'] = access_token
				notification['client_id'] = access_token_data.get("client_id")
				notification['app_code'] = '001'
				notification['message_data'] = json.dumps(notification['message_data'], default=json_super_serializer)
				resp = requests.post(
					url='%s/api/%s/' % ('https://5fea-105-163-157-75.ngrok-free.app', 'send_message'), data=notification,
					verify=False, files=files, timeout=None).text
				print(resp)
				notification_response = json.loads(resp)
				balance = notification_response.get('data', {}).get('balance')
				notification_response = notification_response.get('data', {}).get('confirmation_code', None)
				# if notification_response is None:
				# 	continue
				# if trans is not None:
				# 	notification_responses = getattr(trans, 'notification_response', None)
				# 	if notification_responses is not None:
				# 		notification_responses = notification_responses + "|%s" % notification_response
				# 	else:
				# 		notification_responses = notification_response
				print(f"notification resp {notification_response}")
			# OrganizationService().update(pk=organization.id, sms_balance = balance)
			# else:
			# 	if trans is not None:
			# 		notification_responses = 'Sent'
		return 'success'
	except Exception as e:
		print(traceback.print_exc())
		print("send_notification: %s", e)
	return None


# filePath = "/home/darker/Downloads/Statement015265343320003Aug2022_121815-3.pdf"
filePath = "/home/darker/Downloads/augustino statement-3.pdf"

message_data = {
	"message_template": "em001",
	"message": {
		"salution": "John",
		"corporate": "Menengai limited"
	}
}
files = {'document': open(filePath, 'rb')}
org = "fd5a0a53-96ca-4f70-a7cd-b30a6a3cd8fc"
right_now = datetime.now()
t = right_now.strftime("%Y-%m-%d %H:%M:%S")
recipient = "henrydarker4@gmail.com"

notification_detail = [{
	"destination": recipient, "message_type": '2', 'organization_id': org,
	"lang": 'en', "message_code": 'E00001',  'attached': False, 'subject':"Test Application",
	'message_data' : message_data,

}]


print(send_notification(notification_detail))