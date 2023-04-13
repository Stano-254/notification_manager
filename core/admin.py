from django.contrib import admin

from core.models import State, Country, MessageType, Template, App, Provider, Corporate, MessageLog, AppCredential, \
	OAuth


# Register your models here.
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
	"""
	State model admin.
	Defines the fields to display and which ones are searchable
	"""
	list_display = ('name', 'description', 'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
	list_filter = ('name', 'date_created')
	list_display = ('name', 'code',  'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(MessageType)
class MessageTypeAdmin(admin.ModelAdmin):
	list_filter = ('code',)
	list_display = ('name', 'code', 'state', 'date_modified', 'date_created')
	search_fields = ('code', 'name')


@admin.register(Template)
class TemplateAdmin(admin.ModelAdmin):
	list_filter = ('code',)
	list_display = (
		'code', 'message_type', 'en', 'sw', 'fr', 'editable', 'state', 'date_modified', 'date_created')
	search_fields = ('code',)


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
	list_filter = ('code', 'name',)
	list_display = ('name', 'code', 'state', 'date_modified', 'date_created')
	search_fields = ('code', 'name')


@admin.register(Provider)
class ProviderAdmin(admin.ModelAdmin):
	list_filter = ('name', 'date_created')
	list_display = (
		'name', 'send_url', 'balance_url', 'sms_token_url', 'send_callback', 'balance_callback', 'state', 'key',
		'date_modified', 'date_created')
	search_fields = ('name',)


@admin.register(Corporate)
class CorporateAdmin(admin.ModelAdmin):
	list_filter = ('name', 'provider')
	list_display = ('name', 'core_id', 'provider', 'state', 'date_modified', 'date_created')
	search_fields = ('provider__name',)


@admin.register(MessageLog)
class MessageLogAdmin(admin.ModelAdmin):
	list_filter = ('app', 'date_created')
	list_display = (
		'app', 'corporate', 'destination', 'message', 'message_type', 'confirmation_code', 'source_ip', 'request',
		'response', 'state')
	search_fields = ('corporate__name',)


@admin.register(AppCredential)
class AppCredentialAdmin(admin.ModelAdmin):
	list_filter = ('app', 'corporate')
	list_display = (
		'app', 'corporate', 'message_type', 'username', 'sender_id', 'password', 'org_id', 'user_id',
		'balance',
		'email', 'state')
	search_fields = ('corporate__name',)


@admin.register(OAuth)
class OAuthAdmin(admin.ModelAdmin):
	list_filter = ('app', 'date_created')
	list_display = ('app', 'user', 'access_token', 'state', 'date_modified', 'date_created',)
	search_fields = ('user',)
