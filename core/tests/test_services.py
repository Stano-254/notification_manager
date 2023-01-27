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
		assert state is not None, 'Should have a State object'
