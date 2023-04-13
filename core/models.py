import uuid
from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

from django.conf import settings


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

	class Meta:
		app_label = 'core'

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


class Country(GenericBasemodel):
	"""
	Country model
	"""
	code = models.CharField(max_length=10, blank=True, null=False)

	def __str__(self):
		return f"{self.code}"

	@classmethod
	def default_country(cls):
		try:
			country = cls.objects.get(code="KE")
			return country
		except Exception as e:
			pass
		return None

	class Meta:
		app_label = 'core'


class MessageType(GenericBasemodel):
	"""
	Define different message types
	"""
	code = models.CharField(max_length=10, unique=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name}"


class Template(BaseModel):
	"""
	Defines templates used in  system
	"""
	code = models.CharField(max_length=15, unique=True)
	message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE)
	en = models.TextField(max_length=1500)
	sw = models.TextField(max_length=1500, blank=True, null=True)
	fr = models.TextField(max_length=1500, blank=True, null=True)
	editable = models.BooleanField(default=False)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.code}"


class App(GenericBasemodel):
	"""
	Defines the intergrated apps
	"""
	code = models.CharField(max_length=10, unique=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.code} {self.name}"


class Provider(BaseModel):
	"""
	SMS provider
	"""
	name = models.CharField(max_length=100)
	send_url = models.CharField(max_length=200, blank=True, null=True)
	balance_url = models.CharField(max_length=200, blank=True, null=True)
	sms_token_url = models.CharField(max_length=255, null=True, blank=True)
	send_callback = models.CharField(max_length=50, null=True, blank=True, help_text='send sms endpoint')
	balance_callback = models.CharField(max_length=255)
	state = models.ForeignKey(State, on_delete=models.CASCADE)
	key = models.CharField(default=uuid.uuid4, editable=False, max_length=100)
	date_modified = models.DateTimeField(auto_now=True)
	date_created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.name} - {self.send_callback}"


class Corporate(GenericBasemodel):
	"""
	Defines different corporate
	"""
	core_id = models.CharField(max_length=100)
	provider = models.ForeignKey(Provider, on_delete=models.CASCADE)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.name} - {self.provider.name}"


class MessageLog(BaseModel):
	"""
	Messages logs
	"""
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	corporate = models.ForeignKey(Corporate, blank=True, null=True, on_delete=models.CASCADE)
	destination = models.CharField(max_length=100, blank=True, null=True)
	message = models.TextField(max_length=1500, blank=True, null=True)
	message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE)
	confirmation_code = models.CharField(max_length=60, blank=True, null=True)
	source_ip = models.CharField(max_length=20, blank=True, null=True)
	request = models.CharField(max_length=500, null=True, blank=True)
	response = models.CharField(max_length=250, null=True, blank=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.app} {self.destination}"


class AppCredential(BaseModel):
	"""
	Defines app credentials used to call messaging
	"""
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	corporate = models.ForeignKey(
		Corporate, max_length=100, null=True, blank=True,
		help_text='corporate\'s credentials', on_delete=models.CASCADE)
	message_type = models.ForeignKey(MessageType, on_delete=models.CASCADE)
	username = models.CharField(max_length=100, blank=True, null=True)
	sender_id = models.CharField(max_length=100, blank=True, null=True, help_text='SMS sender id')
	sender_code = models.CharField(max_length=100, null=True, blank=True)
	password = models.CharField(max_length=100, blank=True, null=True)
	org_id = models.CharField(max_length=100, blank=True, null=True)
	user_id = models.CharField(max_length=50, blank=True, null=True, help_text='either user id or sender code')
	balance = models.CharField(max_length=20, blank=True, null=True)
	email = models.CharField(max_length=20, blank=True, null=True)
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.app} {self.message_type}"


def token_expiry():
	"""
	generating token
	:return: time.now() + expiry minute
	:rtype:datetime
	"""
	return timezone.now() + timedelta(minutes=settings.TOKEN_EXPIRY_MINUTES)


class OAuth(BaseModel):
	"""
	Defines different auths
	"""
	app = models.ForeignKey(App, on_delete=models.CASCADE)
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	access_token = models.DateTimeField(default=token_expiry())
	state = models.ForeignKey(State, on_delete=models.CASCADE)

	def __str__(self):
		return f"{self.app} {self.access_token}"

	class Meta:
		verbose_name = 'OAuth'
		verbose_name_plural = "OAuth"