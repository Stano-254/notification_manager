"""
This to test services module
"""
import pytest
#
from mixer.backend.django import mixer

from core.backend.services import StateService

#
# # nonspection SpellCheckingInspection
#
pytestmark = pytest.mark.django_db


class TestStateService(object):

	def test_get(self):
		"""
		Test State get service
		"""
		mixer.blend('core.State', name="Active")
		state = StateService().get(name="Active")
		assert state is not None and state.name == "Active", 'Should have a State object'

	def test_filter(self):
		"""
		Test State filter service
		"""
		mixer.cycle(4).blend('core.State', name="Active")
		state = StateService().filter(name="Active")
		assert len(state) == 4, 'Should have 4 State objects'

	def test_create(self):
		"""
		Test StateService create() method
		"""
		state = StateService().create(name="Active")
		assert state is not None, 'Should have a State object'

	def test_update(self):
		"""
		Test StateService update() method
		"""
		status = mixer.blend('core.State', name="Active")
		state = StateService().update(status.id, name="Completed")
		assert state is not None and state.name == "Completed",  'Should have an updated  State object'
