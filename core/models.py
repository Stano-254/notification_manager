import uuid

from django.db import models


# Create your models here.


class BaseModel(models.Model):
	"""
	Defines repetitive fields for the other models
	"""
	id = models.UUIDField(max_length=100, default=uuid.uuid4, unique=True, editable=False, primary_key=True)
	date_modified = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

	class Meta(object):
		abstract = True


class GenericBasemodel(BaseModel):
	"""
	Defines repetetive fields to ensure reuse
	"""
	name = models.CharField(max_length=100)
	description = models.TextField(max_length=255, blank=True, null=True)

	class Meta(object):
		abstract = True


class State(GenericBasemodel):
	"""
	Defines different state within lifecyle of the system
	"""
	def __str__(self):
		return f"{self.name}"


	@classmethod
	def default_state(cls):
		"""
		presets default states for the models that needs it before being created
		:return:
		"""
		try:
			state = cls.objects.get(name="Active")
			return state
		except Exception as e:
			state = cls.objects.create(name="Active")
		return state

	@classmethod
	def disabled_state(cls):
		"""
		auto disable state for models on user
		:return:
		"""
		try:
			state = cls.objects.get(name="Disabled")
			return state
		except Exception as e:
			state = cls.objects.create(name="Disabled")
			return state