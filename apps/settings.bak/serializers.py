from rest_framework import serializers


class MailTestSerializer(serializers.Serializer):
    EMAIL_HOST = serializers.CharField(max_length=1024, required=True)
    EMAIL_PORT = serializers.IntegerField(default=25)
    EMAIL_HOST_USER = serializers.CharField(max_length=1024)
    EMAIL_HOST_PASSWORD = serializers.CharField(required=False, allow_blank=True)
    EMAIL_FROM = serializers.CharField(required=False, allow_blank=True)
    EMAIL_RECIPIENT = serializers.CharField(required=False, allow_blank=True)
    EMAIL_USE_SSL = serializers.BooleanField(default=False)
    EMAIL_USE_TLS = serializers.BooleanField(default=False)


class LDAPTestSerializer(serializers.Serializer):
    AUTH_LDAP_SERVER_URI = serializers.CharField(max_length=1024)
    AUTH_LDAP_BIND_DN = serializers.CharField(max_length=1024, required=False, allow_blank=True)
    AUTH_LDAP_BIND_PASSWORD = serializers.CharField(required=False, allow_blank=True)
    AUTH_LDAP_SEARCH_OU = serializers.CharField()
    AUTH_LDAP_SEARCH_FILTER = serializers.CharField()
    AUTH_LDAP_USER_ATTR_MAP = serializers.CharField()
    AUTH_LDAP_START_TLS = serializers.BooleanField(required=False)
    
class LDAPTestUserSerializer(serializers.Serializer):
    AUTH_LDAP_USERNAME_PASSWORD = serializers.CharField(max_length=1024)
    AUTH_LDAP_USER_NAME = serializers.CharField(max_length=1024)

class LDAPUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    existing = serializers.BooleanField(read_only=True)


class PublicSettingSerializer(serializers.Serializer):
    data = serializers.DictField(read_only=True)
