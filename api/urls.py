"""
The URLs for the API.
"""
from django.conf.urls import url

from api.views import send_message, get_access_token

urlpatterns = [
	url(r'^send_message/', send_message),
	url(r'^get_access_token/', get_access_token),

]
