import json

from mixer.backend.django import mixer
from django.contrib.auth.models import User
from django.test import Client, RequestFactory
from api.decorators import authentication_wrapper
from api.oauth import OAuth
import pytest
from mock import Mock

pytestmark = pytest.mark.django_db


class TestOAUTH(object):

	def test_generate_account_toke(self):
		self.user = mixer.blend(User, password="Cosmic3421$#")
		state = mixer.blend('core.State', name="Active")
		app = mixer.blend('core.App', name='ecommerce', state=state)
		assert OAuth().generate_account_token(access_app=app, user=self.user) is not None, 'should generate a token'

	def test_valid_account_access_token(self):
		self.test_generate_account_toke()
		assert OAuth.get_valid_account_access_token(user=self.user) is not None, 'Should return an Oauth object'

	def test_authentication_wrapper(self):
		user = mixer.blend(User, password="Cosmic3421$#", username="ecommerce")
		state = mixer.blend('core.State', name="Active")
		mixer.blend('core.App', name='Ecommerce', state=state, id="5369a2c6-bd9f-4d90-9575-bc0bab87b1c5")
		res_data = {
			"username": 'ecommerce',
			'client_secret': 'Cosmic3421$#',
			'client_id': '5369a2c6-bd9f-4d90-9575-bc0bab87b1c5'
		}
		func = Mock(return_value='response')
		decorated_func = authentication_wrapper(func)
		self.factory = RequestFactory()
		request = self.factory.post(
			'/api/send_message/', data=json.dumps(res_data), content_type='application/json')
		decorated_func(request)
		assert not func.called, 'assert response is redirected to the decorator'
