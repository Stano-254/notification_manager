import json

from api.backend.notification_processor import Processor
from mixer.backend.django import mixer
import pytest
pytestmark = pytest.mark.django_db


class TestNotificationProcessor(object):
	"""
	Test for notification processor
	"""

	def test_replace_tags(self):
		"""
		test for replace tags method
		:return:
		"""
		# noinspection SpellCheckingInspection
		assert Processor.replace_tags('Hello [salutation]', salutation='John') == 'Hello John', \
			'should successfully replace tag'

	def test_send_message(self):
		state = mixer.blend('core.State', name='Active')
		mixer.blend('core.State', name='Complete')
		mixer.blend('core.App', name='Failed')
		app = mixer.blend('core.App', name='Ecommerce', code='01', state=state)
		message_type = mixer.blend(
			'core.MessageType', name="EMAIL", code='1234', state=state)
		app_cred = mixer.blend(
			'core.AppCredential', app=app, email='stanoemali87@gmail.com', password="qisiebnrbeudsopr",
			message_type=message_type, state=state)
		mixer.blend(
			'core.Template', code='1345', state=state, en='[message]'
		)
		destination = 'henrydarker4@gmail.com'
		source_ip = "127.0.0.1"
		message_data = {
			"message_template": "em001",
			"message": {
				"salutation": "John",
				"corporate": "Menengai limited"
			}
		}
		request = {}
		assert Processor().send_message(
			app_code='01', message_code='1345', type_code='1234', destination=destination, corporate_id=app_cred.corporate,
			request=request, message_data=json.dumps(message_data), source_ip=source_ip, lang='en', cc=None,
		).get('code', '') == '100.000.000', 'success code'
