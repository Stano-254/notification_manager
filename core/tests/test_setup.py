from unittest import TestCase

from mixer.backend.django import mixer


class TestSetUp(TestCase):
	"""
	Class for setting up test variables
	"""

	def setUp(self):
		self.state_disabled = mixer.blend('core.State', name="Disabled")
		self.state_active = mixer.blend('core.State', name="Active")
		self.state_completed = mixer.blend('core.State', name="Completed")

	def tearDown(self):
		return super().tearDown()


