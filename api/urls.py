"""
The URLs for the API.
"""

from django.urls import path
from api.views import send_message, get_access_token

urlpatterns = [
	path('send_message/', send_message),
	path('get_access_token/', get_access_token),

]
