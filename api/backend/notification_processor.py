"""
handles notification logic
sending out emails and sms
"""
import json
import logging

from api.backend.utils import generate_confirmation_key
from core.backend.services import TemplateService, MessageTypeService, AppService

lgr = logging.getLogger(__name__)


class Processor(object):
	"""
	handles notification logic
	"""

	@staticmethod
	def replace_tags(templates_string, **kwargs):
		"""
		Replaces replace_tags with passed in arguments
		:param templates_string: the template string to be replaced
		:type templates_string: str
		:param kwargs: the keyword arguments representing the tag in the string without []
		:return: The Template string replaced accordingly
		:rtype: str
		"""
		try:
			for k, v in kwargs.items():
				templates_string = templates_string.replace('[%s]' % str(k), str(v))
			return templates_string
		except Exception as e:
			lgr.exception(f"replace tags Exception: {e}")

	def send_message(
			self, app_code, message_code, type_code, destination, request, replace_tags, source_ip, lang, corporate_id,
			subject=None):
		"""
		- verify and validates the params ,
		- calls replace tags on the message
		- send the message after creating the record in database
		:param app_code: application identifier
		:param message_code: message code to be used
		:param type_code: message type to used SMS or EMAIL
		:param destination: recipient of the message
		:param request: raw request from sender / application
		:param replace_tags: dictionary of message with data to be replaced
		:param source_ip: ip address of the sender
		:param lang: language of the template to use
		:param corporate_id: organization id
		:param subject: the subject of the Message
		:return: response code
		"""
		try:
			message = TemplateService().get(code=message_code)
			clean_replace_tags = json.loads(replace_tags)
			if message is None:
				return {'code': '400.100.100'}
			template = getattr(message, lang, '')
			message = self.replace_tags(template, **clean_replace_tags)
			message = self.replace_tags(message, **clean_replace_tags)
			message_type = MessageTypeService().get(code=type_code, state__name="Active")
			if not message_type:
				return {'code': '400.100.102'}
			app = AppService().get(code=app_code, state__name="Active")
			if not app:
				return {'code': '400.100.103'}
			confirmation_code = generate_confirmation_key()
			log_message = self.log_message(
				app=app, destination=destination, message=message, source_ip=source_ip, request=request,
				message_type=message_type, confirmation_code=confirmation_code, corporate_id=corporate_id)


		except Exception as e:
			pass

	@staticmethod
	def log_message(app, destination, message, source_ip, request, message_type, confirmation_code, corporate_id, ):
		pass
		return 1
