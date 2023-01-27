# -*- coding: utf-8 -*-
"""
This is the service base from which all CRUD services inherit from.
"""
import logging

lgr = logging.getLogger(__name__)


class ServiceBase(object):
	"""
	The class to handle CRUD methods.
	"""

	manager = None
	"""
	The manager for the model. e.g. for Account module, set this as Account.objects
	"""

	def __init__(self, lock_for_update = False):
		"""
		Initializes the service to determine whether this transaction should be locked for the retrieved objects or not.
		@param lock_for_update: A sentinel determining whether to lock this model. Defaults to False
		@type lock_for_update: bool
		"""
		super(ServiceBase, self).__init__()
		if lock_for_update and self.manager is not None:
			self.manager = self.manager.select_for_update()

	def get(self, *args, **kwargs):
		"""
		This method gets a single record from the DB using the manager.
		:param args: Arguments to pass to the get method.
		:param kwargs: key=>value methods to pass to the get method.
		:return: Manager object instance or None on error.
		"""
		try:
			if self.manager is not None:
				return self.manager.get(*args, **kwargs)
		except Exception as e:
			print('%sService get exception: %s' % (self.manager.model.__name__, e))
		return None

	def filter(self, *args, **kwargs):
		"""
		This method returns a queryset of the objects as from the manager.
		:param args: Arguments to pass to the filter method.
		:param kwargs: key=>value methods to pass to the filter method.
		:return: Queryset or None on error
		:rtype: Queryset | None
		"""
		try:
			if self.manager is not None:
				return self.manager.filter(*args, **kwargs)
		except Exception as e:
			lgr.error('%sService filter exception: %s' % (self.manager.model.__name__, e))
		return None

	def create(self, **kwargs):
		"""
		This method creates an entry with the given kwargs as for the given manager.
		:param kwargs: key=>value methods to pass to the create method.
		:return: Created object or None on error.
		"""
		try:
			if self.manager is not None:
				return self.manager.create(**kwargs)
		except Exception as e:
			lgr.error('%sService create exception: %s' % (self.manager.model.__name__, e))
		return None

	def update(self, pk, **kwargs):
		"""
		Updates the record with the given key.
		:param pk: The id for the record to update.
		:param kwargs: The params to update the record with.
		:return: The updated record or None on error.
		"""
		try:
			record = self.get(id=pk)
			if record is not None:
				for k, v in kwargs.items():
					setattr(record, k, v)
				record.save()
				record.refresh_from_db()
				return record
		except Exception as e:
			lgr.error('%sService update exception: %s' % (self.manager.model.__name__, e))
		return None
