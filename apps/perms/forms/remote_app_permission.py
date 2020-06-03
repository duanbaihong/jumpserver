#  coding: utf-8
#

from django.utils.translation import ugettext as _
from django import forms
from orgs.mixins.forms import OrgModelForm
from assets.models import SystemUser

from ..models import RemoteAppPermission


__all__ = [
    'RemoteAppPermissionCreateUpdateForm',
]


class RemoteAppPermissionCreateUpdateForm(OrgModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        users_field = self.fields.get('users')
        if self.instance:
            users_field.queryset = self.instance.users.all()
        else:
            users_field.queryset = []

        # 过滤系统用户
        system_users_field = self.fields.get('system_users')
        system_users_field.queryset = SystemUser.objects.filter(
            protocol=SystemUser.PROTOCOL_RDP
        )

    class Meta:
        model = RemoteAppPermission
        exclude = (
            'id', 'date_created', 'created_by', 'org_id'
        )
        widgets = {
            'users': forms.SelectMultiple(
                attrs={'class': 'users-select2', 'data-placeholder': _('User')}
            ),
            'user_groups': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('User group')}
            ),
            'remote_apps': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('RemoteApp')}
            ),
            'system_users': forms.SelectMultiple(
                attrs={'class': 'select2', 'data-placeholder': _('System user')}
            )
        }
