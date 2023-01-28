# -*- coding: utf-8 -*-
"""
This is the service module from which all CRUD core services are declared.
"""

from core.backend.servicebase import ServiceBase
from core.models import State, MessageType, Template, MessageLog, AppCredential, App, OAuth, Provider, Corporate


class StateService(ServiceBase):
	"""
	State model CRUD services
	"""
	manager = State.objects


class MessageTypeService(ServiceBase):
	"""
	Messagetype model CRUD services
	"""
	manager = MessageType.objects


class TemplateService(ServiceBase):
	"""
	Template model CRUD service
	"""
	manager = Template.objects


class AppService(ServiceBase):
	"""
	App model CRUD service
	"""
	manager = App.objects


class ProviderService(ServiceBase):
	"""
	Provider model CRUD service
	"""
	manager = Provider.objects


class CorporateService(ServiceBase):
	"""
	Corporate model CRUD service
	"""
	manager = Corporate.objects


class MessageLogService(ServiceBase):
	"""
	MessageLog model CRUD service
	"""
	manager = MessageLog.objects


class AppCredentialService(ServiceBase):
	"""
	AppCredentials model CRUD service
	"""
	manager = AppCredential.objects


class OAuthService(ServiceBase):
	"""
	OAuth model CRUD service
	"""
	manager = OAuth.objects
