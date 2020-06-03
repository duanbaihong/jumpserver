# coding: utf-8
# 

from rest_framework import serializers

__all__ = [
    'LDAPTestConfigSerializer', 'LDAPUserSerializer', 'LDAPTestLoginSerializer','LDAPTestUserSerializer'
]


class LDAPTestConfigSerializer(serializers.Serializer):
    AUTH_LDAP_SERVER_URI = serializers.CharField(max_length=1024)
    AUTH_LDAP_BIND_DN = serializers.CharField(max_length=1024, required=False, allow_blank=True)
    AUTH_LDAP_BIND_PASSWORD = serializers.CharField(required=False, allow_blank=True)
    AUTH_LDAP_SEARCH_OU = serializers.CharField()
    AUTH_LDAP_SEARCH_FILTER = serializers.CharField()
    AUTH_LDAP_USER_ATTR_MAP = serializers.CharField()
    AUTH_LDAP_START_TLS = serializers.BooleanField(required=False)
    AUTH_LDAP = serializers.BooleanField(required=False)


class LDAPTestLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=1024, required=True)
    password = serializers.CharField(max_length=2014, required=True)


class LDAPUserSerializer(serializers.Serializer):
    id = serializers.CharField()
    username = serializers.CharField()
    name = serializers.CharField()
    email = serializers.CharField()
    existing = serializers.BooleanField(read_only=True)

class LDAPTestUserSerializer(serializers.Serializer):
    AUTH_LDAP_USERNAME_PASSWORD = serializers.CharField(max_length=1024)
    AUTH_LDAP_USER_NAME = serializers.CharField(max_length=1024)

