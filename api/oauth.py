import logging
from django.db.utils import OperationalError
from api.backend.utils import generate_token
from django.utils import timezone
from core.backend.services import OAuthService, StateService

lgr = logging.getLogger(__name__)


class OAuth(object):
	"""
	class for OAuth
	"""
	@staticmethod
	def generate_account_token(access_app, user):
		"""
		Generates an access token and stores it for this account for set validity period
		:param access_app:
		:param user:
		:return:
		"""
		try:
			if access_app:
				try:
					OAuthService().filter(app=access_app, user=user).delete()
				except OperationalError as err:
					lgr.exception(f"Unable to get auth data:{err}")
				return OAuthService().create(
					user=user, app=access_app, access_token=generate_token(),
					state=StateService().get(name="Active"))
		except OperationalError as e:
			lgr.exception(f'generate_account_token:Exception {e}')
		return None

	@staticmethod
	def get_valid_account_access_token(user):
		"""
		get a valid access token for given account else return None
		:param user: user model
		:return: OAuth instance
		"""
		try:
			return OAuthService().filter(
				user=user, expires_at__gt=timezone.now()).order_by('-date_created').first()
		except Exception as e:
			lgr.exception(f'get_valid_account_access_token Exception: {e}')
		return None
