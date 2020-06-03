# coding: utf-8
# 

from django import forms
from django.utils.translation import ugettext_lazy as _

from common.fields import FormDictField, FormEncryptCharField
from .base import BaseForm


__all__ = ['LDAPSettingForm','LDAPTestforUsername']


class LDAPTestforUsername(BaseForm):
    """docstring for LDAPTestforUsername"""
    AUTH_LDAP_USER_NAME = forms.CharField(
        label=_("LDAP UserName"),
        widget=forms.TextInput(attrs={'placeholder': _("Username")}),
        help_text=_("Connect LDAP Username")
    )

    AUTH_LDAP_USERNAME_PASSWORD = FormEncryptCharField(
        label=_("LDAP User Password"),
        widget=forms.PasswordInput(attrs={'placeholder': _("Password")}),
        help_text=_("Connect LDAP User Password")
    )
        
class LDAPSettingForm(BaseForm):
    AUTH_LDAP = forms.BooleanField(label=_("Enable LDAP auth"), required=False)
    AUTH_LDAP_SERVER_URI = forms.CharField(
        label=_("LDAP server"),
        widget=forms.TextInput(attrs={'placeholder': 'ldap://[ip]:389|ip'}),
    )
    AUTH_LDAP_BIND_DN = forms.CharField(
        label=_("Bind DN"),
        widget=forms.TextInput(attrs={'placeholder': 'cn=admin,dc=xxxx,dc=com'}),
    )
    AUTH_LDAP_BIND_PASSWORD = FormEncryptCharField(
        label=_("Bind Password"),
        widget=forms.PasswordInput(attrs={'placeholder': _("Bind Password")}), required=False
    )
    AUTH_LDAP_SEARCH_OU = forms.CharField(
        label=_("User OU"),
        widget=forms.TextInput(attrs={'placeholder': 'ou=xxxx,dc=xxxx,dc=com'}),
        help_text=_("Use | split User OUs")
    )
    AUTH_LDAP_SEARCH_FILTER = forms.CharField(
        label=_("User search filter"),
        widget=forms.TextInput(attrs={'placeholder': '(uid=%(user)s)'}),
        help_text=_("Choice may be (cn|uid|sAMAccountName)=%(user)s)")
    )

    AUTH_LDAP_USER_ATTR_MAP = FormDictField(
        label=_("User attr map"),
        widget=forms.Textarea(attrs={
            'placeholder': '{"username": "uid", "name": "sn", "email": "mail", "role": "businessCategory", "phone": "mobile", "_public_key": "sshPublickey"}',
            'style':'resize:none'}),
        help_text=_(
            "User attr map present how to map LDAP user attr to jumpserver, "
            "username,name,email is jumpserver attr"
        ),
    )

    AUTH_LDAP_GROUP_SEARCH_OU = forms.CharField(
        label=_("Group OU"),
        widget=forms.TextInput(attrs={'placeholder': 'ou=xxxx,dc=xxxx,dc=com'}),
        help_text=_("Group search base OU")
    )
    GROUP_TYPE_STRING_CHOICES=(
            ('PosixGroupType','PosixGroupType'),
            ('GroupOfNamesType','GroupOfNamesType'),
            ('GroupOfUniqueNamesType','GroupOfUniqueNamesType'),
            ('ActiveDirectoryGroupType','ActiveDirectoryGroupType'),
            ('OrganizationalRoleGroupType','OrganizationalRoleGroupType'),
            ('NestedGroupOfNamesType','NestedGroupOfNamesType'),
            ('NestedGroupOfUniqueNamesType','NestedGroupOfUniqueNamesType'),
            ('NestedActiveDirectoryGroupType','NestedActiveDirectoryGroupType'),
            ('NestedOrganizationalRoleGroupType','NestedOrganizationalRoleGroupType'),
                               )
    AUTH_LDAP_GROUP_TYPE_STRING= forms.ChoiceField(
        label=_("LDAP Group Type"),
        choices=GROUP_TYPE_STRING_CHOICES,
        widget=forms.Select(attrs={'class':'form-control','style':"padding-right:22px;appearance: none;-moz-appearance: none;-webkit-appearance: none;"}),
        help_text=_("LDAP group type selection,default attr is 'cn'.Configuration parameters: AUTH_LDAP_GROUP_TYPE_STRING='cn'")
    )

    AUTH_LDAP_GROUP_TYPE_STRING_ATTR = forms.CharField(
        initial='cn',
        widget=forms.TextInput(attrs={'placeholder': 'cn','class':'form-control','style':'width:140px'}),
    )

    AUTH_LDAP_GROUP_SEARCH_FILTER = forms.CharField(
        label=_("Group search filter"),
        widget=forms.TextInput(attrs={'placeholder': '(& (cn=%(user)s) (| (objectclass=groupOfNames) (objectclass=groupOfUniqueNames) (objectclass=posixGroup)))'}),
        required=False,
        help_text=_("Group filter condition.Example:(& (cn=%(user)s) (| (objectclass=groupOfNames) (objectclass=groupOfUniqueNames) (objectclass=posixGroup)))"
            )
    )
    # AUTH_LDAP_GROUP_SEARCH_OU = CONFIG.AUTH_LDAP_GROUP_SEARCH_OU
    # AUTH_LDAP_GROUP_SEARCH_FILTER = CONFIG.AUTH_LDAP_GROUP_SEARCH_FILTER
    AUTH_LDAP_MIRROR_GROUPS = forms.BooleanField(
        label=_("Sync LDAP User Group Info to Database"), 
        help_text=_(
            "If the group information exists, it will not be synchronized,"
            "if it does not exist,it will be synchronized. If it is a new group,"
            "administrators need to go to the background to allocate host privileges."
            "Only then can the relevant host be accessed. "
            "Configuration parameters: AUTH_LDAP_MIRROR_GROUP = True | False"
        ),
        required=False
    )
    AUTH_LDAP_START_TLS = forms.BooleanField(
        label=_("Use SSL"), required=False
    )
