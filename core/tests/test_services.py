"""
This to test services module
"""
import datetime

import pytest
#
from mixer.backend.django import mixer

from core.backend.services import StateService, MessageTypeService, TemplateService, AppService, ProviderService
from core.tests.test_setup import TestSetUp

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestStateService(object):
	@staticmethod
	def test_get():
		"""
		Test State get service
		"""
		mixer.blend('core.State', name="Active")
		state = StateService().get(name="Active")
		assert state is not None and state.name == "Active", 'Should have a State object'

	@staticmethod
	def test_filter():
		"""
		Test State filter service
		"""
		mixer.cycle(4).blend('core.State', name="Active")
		state = StateService().filter(name="Active")
		assert len(state) == 4, 'Should have 4 State objects'

	@staticmethod
	def test_create():
		"""
		Test StateService create() method
		"""
		state = StateService().create(name="Active")
		assert state is not None, 'Should have a State object'

	@staticmethod
	def test_update():
		"""
		Test StateService update() method
		"""
		status = mixer.blend('core.State', name="Active")
		state = StateService().update(status.id, name="Completed")
		assert state is not None and state.name == "Completed", 'Should have an updated  State object'


class TestMessageTypeService(TestSetUp):
	def test_get(self):
		mixer.blend('core.MessageType', name="SMS", code="SMS", state=self.state_active)
		message_type = MessageTypeService().get(code="SMS")
		self.assertIsNotNone(message_type), "Should have message type"

	def test_filter(self):
		mixer.cycle(4).blend('core.MessageType', state=self.state_active)
		messages = MessageTypeService().filter()
		self.assertEqual(len(messages), 4), "Should return 4 message_types"

	def test_create(self):
		message_type = MessageTypeService().create(name="Email", code="EMAIL", state=self.state_active)
		self.assertIsNotNone(message_type), "Should create message_type"

	def test_update(self):
		message = mixer.blend('core.MessageType', name="Email", code="Email", state=self.state_active)
		updated_msg_type = MessageTypeService().update(message.id, code="EMAIL")
		self.assertEqual(updated_msg_type.code, "EMAIL"), "Should return an updated message type"


class TestTemplateService(TestSetUp):
	"""
	Test for TemplateService
	"""

	def test_get(self):
		mixer.blend('core.Template', code="ETL", state=self.state_active)
		template = TemplateService().get(code="ETL")
		self.assertIsNotNone(template), "Should return a single template object"

	def test_filter(self):
		mixer.cycle(4).blend('core.Template', state=self.state_active)
		templates = TemplateService().filter(state=self.state_active)
		self.assertEqual(len(templates), 4), "Should return 4 templates"

	def test_create(self):
		message_type = mixer.blend('core.MessageType', state=self.state_active)
		template = TemplateService().create(
			code="ETL", message_type=message_type, en="this should be good", state=self.state_active)
		self.assertIsNotNone(template), "Should create template"

	def test_update(self):
		template = mixer.blend('core.Template', code='ETL', state=self.state_active)
		updated_template = TemplateService().update(template.id, code="ERD")
		self.assertEqual(updated_template.code, "ERD"), "Should update and return updated template"


class TestAppService(TestSetUp):
	"""
	Test for App service
	"""

	def test_get(self):
		mixer.blend('core.App', name="Weko", state=self.state_active)
		app = AppService().get(name='Weko')
		self.assertIsNotNone(app), "Should return an App object"

	def test_filter(self):
		mixer.cycle(4).blend('core.App', state=self.state_active)
		apps = AppService().filter(state=self.state_active)
		self.assertIsNotNone(len(apps), 4), "Should return 4 objects"

	def test_create(self):
		app = AppService().create(
			name="Zuku", code="Zuku", state=self.state_active)
		self.assertIsNotNone(app), "Should create an app instance"

	def test_update(self):
		app = mixer.blend('core.App', state=self.state_active)
		updated_app = AppService().update(app.id, code="ZUKU")
		self.assertEqual(updated_app.code, "ZUKU"), "Should return an updated app instance"


class TestProviderService(TestSetUp):
	"""
	ProviderService tests
	"""

	def test_get(self):
		mixer.blend('core.Provider', name="Africa's Taking", state=self.state_active)
		provider = ProviderService().get(state=self.state_active)
		self.assertIsNotNone(provider), "Should return an provider instance"

	def test_filter(self):
		mixer.cycle(4).blend('core.Provider', state=self.state_active)
		providers = ProviderService().filter(state=self.state_active)
		self.assertEqual(len(providers), 4), "Should return 4  providers"

	def test_create(self):
		provider = ProviderService().create(
			name="Africas", balance_url="send_balance_", state=self.state_active,
			date_modified=datetime.date, date_created=datetime.date)
		self.assertIsNotNone(provider), "Should create a provider object"

	def test_update(self):
		provider = mixer.blend('core.Provider', state=self.state_active)
		updated_provider = ProviderService().update(provider.id, name="Denko")
		self.assertEqual(updated_provider.name, 'Denko'), "Should update provider object"


class TestCorporateService(TestSetUp):
	"""
	ProviderService tests
	"""

	def test_get(self):
		pass

	def test_filter(self):
		pass

	def test_create(self):
		pass

	def test_update(self):
		pass


class TestMessageLogService(TestSetUp):
	"""
	ProviderService tests
	"""

	def test_get(self):
		pass

	def test_filter(self):
		pass

	def test_create(self):
		pass

	def test_update(self):
		pass


class TestAppCredentialService(TestSetUp):
	"""
	ProviderService tests
	"""

	def test_get(self):
		pass

	def test_filter(self):
		pass

	def test_create(self):
		pass

	def test_update(self):
		pass


class TestOAuthService(TestSetUp):
	"""
	ProviderService tests
	"""

	def test_get(self):
		pass

	def test_filter(self):
		pass

	def test_create(self):
		pass

	def test_update(self):
		pass
