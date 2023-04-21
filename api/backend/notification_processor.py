"""
handles notification logic
sending out emails and sms
"""
import json
import logging

from api.backend.email_sender import EmailSender
from api.backend.utils import generate_confirmation_key, validate_email
from core.backend.services import TemplateService, MessageTypeService, AppService, AppCredentialService, \
	CorporateService, MessageLogService, StateService

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
			self, app_code, message_code, type_code, destination, request, replace_tags, source_ip, lang, corporate_id, cc,
			subject=None, attachment=None):
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
			if not log_message:
				return {'code': '400.100.104'}
			if str(message_type.name).upper() == "EMAIL":
				if not validate_email(destination):
					return {'code': '400.100.105'}
				app_credentials = AppCredentialService().filter(
					app=app, state__name="Active", message_type=message_type).first()
				# corporate = CorporateService().get(core_id=corporate_id)
				if not app_credentials:
					return {'code': '400.100.106'}
				from_address = app_credentials.email
				name = (" - " + app_credentials.corporate.name) if app_credentials.corporate else ""
				subject = f'Email Notification {name}' if not subject else subject
				email = EmailSender().send_email(
					recipient_email=destination, subject=subject, message=message, reply_to=from_address, attachment=attachment,
					sender=app_credentials.sender_id, from_address=from_address, cc=cc, password=app_credentials.password)
				if email.get('status', '') == 'success':
					self.update_log_message(log_message=log_message, response=json.dumps(email))
					return {'code': '100.000.000', 'data': {'confirmation_code': confirmation_code}}
				else:
					self.update_log_message(log_message=log_message, status='failed', response=json.dumps(email))
					return {'code': '400.100.107'}

		except Exception as e:
			lgr.exception(f"Failed to send the notification : {e}")

	@staticmethod
	def log_message(app, destination, message, source_ip, request, message_type, confirmation_code='',
					corporate_id=None):
		"""
		Saves the message that is being transmitted to the database
		:param app: message origin app
		:param destination: recipient of the message
		:param message: message content
		:param source_ip: ip address of the sender
		:param request: raw request form sender
		:param message_type: messageType model object
		:param confirmation_code:
		:param corporate_id:
		:return: created object
		"""
		try:
			state = StateService().get(name="Active")
			corporate = None
			if corporate_id:
				corporate = CorporateService().get(core_id=corporate_id)
			return MessageLogService().create(
				app=app, destination=destination, message=message, source_ip=source_ip, state=state, request=request,
				message_type=message_type, confirmation_code=confirmation_code, corporate=corporate)
		except Exception as e:
			lgr.exception(f"Log message error : {e}")
		return None

	@staticmethod
	def update_log_message(log_message, status='Complete', response=None):
		"""
		updates the log message as failed or completed
		:param log_message: transaction
		:param status: transaction state,
		:param response: feedback from notification sent
		:return: LogMessage | None
		"""
		try:
			state= StateService().get(name=str(status).title())
			return MessageLogService().update(log_message.id, state=state,response=response)
		except Exception as e:
			lgr.exception(f"Failed to update transaction: {e}")
		return None
