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
