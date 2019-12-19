# coding:utf-8
#

import ldap
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured, ObjectDoesNotExist
from django_auth_ldap.backend import _LDAPUser, LDAPBackend
from django_auth_ldap.config import _LDAPConfig, LDAPSearch, LDAPSearchUnion, PosixGroupType, GroupOfNamesType, GroupOfUniqueNamesType, OrganizationalRoleGroupType, NestedGroupOfNamesType, NestedGroupOfUniqueNamesType, NestedOrganizationalRoleGroupType
from users.models import UserGroup
from users.models.user import RoleMixin
from common.utils import get_signer, validate_ssh_public_key

from users.utils import construct_user_email
logger = _LDAPConfig.get_logger()


class LDAPAuthorizationBackend(LDAPBackend):
    """
    Override this class to override _LDAPUser to LDAPUser
    """
    def __init__(self):
        # 用数据信息保存GROUP_TYPE 信息
        if not self.settings.GROUP_TYPE and hasattr(settings,'AUTH_LDAP_GROUP_TYPE_STRING') and hasattr(settings,'AUTH_LDAP_GROUP_TYPE_STRING_ATTR'):
            self.settings.GROUP_TYPE = globals().get(settings.AUTH_LDAP_GROUP_TYPE_STRING)(name_attr=settings.AUTH_LDAP_GROUP_TYPE_STRING_ATTR)

        # 用数据信息保存GROUP_SEARCH 信息
        self.settings.GROUP_SEARCH = LDAPSearch(
            settings.AUTH_LDAP_GROUP_SEARCH_OU, ldap.SCOPE_SUBTREE, settings.AUTH_LDAP_GROUP_SEARCH_FILTER
          )


    def authenticate(self, request=None, username=None, password=None, **kwargs):
        if password or self.settings.PERMIT_EMPTY_PASSWORD:
            ldap_user = LDAPUser(self, username=username.strip(), request=request)
            user = self.authenticate_ldap_user(ldap_user, password)
        else:
            logger.debug('Rejecting empty password for {}'.format(username))
            user = None

        return user

    def get_user(self, user_id):
        user = None

        try:
            user = self.get_user_model().objects.get(pk=user_id)
            LDAPUser(self, user=user)  # This sets user.ldap_user
        except ObjectDoesNotExist:
            pass

        return user

    def get_group_permissions(self, user, obj=None):
        if not hasattr(user, 'ldap_user') and self.settings.AUTHORIZE_ALL_USERS:
            LDAPUser(self, user=user)  # This sets user.ldap_user

        if hasattr(user, 'ldap_user'):
            permissions = user.ldap_user.get_group_permissions()
        else:
            permissions = set()

        return permissions

    def populate_user(self, username):
        ldap_user = LDAPUser(self, username=username)
        user = ldap_user.populate_user()

        return user


class LDAPUser(_LDAPUser):

    def _search_for_user_dn(self):
        """
        This method was overridden because the AUTH_LDAP_USER_SEARCH
        configuration in the settings.py file
        is configured with a `lambda` problem value
        """
        user_search_union = [
            LDAPSearch(
                USER_SEARCH, ldap.SCOPE_SUBTREE,
                settings.AUTH_LDAP_SEARCH_FILTER
            )
            for USER_SEARCH in str(settings.AUTH_LDAP_SEARCH_OU).split("|")
        ]

        search = LDAPSearchUnion(*user_search_union)
        if search is None:
            raise ImproperlyConfigured(
                'AUTH_LDAP_USER_SEARCH must be an LDAPSearch instance.'
            )

        results = search.execute(self.connection, {'user': self._username})
        if results is not None and len(results) == 1:
            (user_dn, self._user_attrs) = next(iter(results))
        else:
            user_dn = None

        return user_dn

    def _populate_user_from_attributes(self):
        super()._populate_user_from_attributes()
        if hasattr(self._user,'public_key') and getattr(self._user,'public_key') != "":
            if(validate_ssh_public_key(getattr(self._user,'public_key'))):
                signer = get_signer()
                public_key_sign=signer.sign(self._user.public_key)
                setattr(self._user,'public_key',public_key_sign)
            else:
                setattr(self._user,'public_key','')
                logger.error("The public key obtained from LDAP is invalid and the \"public_key\" field mapping is skipped.")
        if not hasattr(self._user, 'email') or '@' not in self._user.email:
            email = '{}@{}'.format(self._user.username, settings.EMAIL_SUFFIX)
            setattr(self._user, 'email', email)

    def _get_or_create_user(self, force_populate=False):
        super()._get_or_create_user()
        target_group_names = frozenset(self._get_groups().get_group_names())
        if 'Jumpserver-admin' in target_group_names:
            setattr(self._user,'role',RoleMixin.ROLE_ADMIN)
        else:
            setattr(self._user,'role',RoleMixin.ROLE_USER)
        self._user.save()
        if not self.settings.MIRROR_GROUPS:
            new_groups = UserGroup.objects.filter(name__in=target_group_names)
            if new_groups:
                self._user.groups.set(new_groups)

 
    def _mirror_groups(self):
        """
        Mirrors the user's LDAP groups in the Django database and updates the
        user's membership.
        """
        
        target_group_names = frozenset(self._get_groups().get_group_names())
        current_group_names = frozenset(
            self._user.groups.values_list("name", flat=True).iterator()
        )
        # These were normalized to sets above.
        MIRROR_GROUPS_EXCEPT = self.settings.MIRROR_GROUPS_EXCEPT
        MIRROR_GROUPS = self.settings.MIRROR_GROUPS

        # If the settings are white- or black-listing groups, we'll update
        # target_group_names such that we won't modify the membership of groups
        # beyond our purview.
        if isinstance(MIRROR_GROUPS_EXCEPT, (set, frozenset)):
            target_group_names = (target_group_names - MIRROR_GROUPS_EXCEPT) | (
                current_group_names & MIRROR_GROUPS_EXCEPT
            )
        elif isinstance(MIRROR_GROUPS, (set, frozenset)):
            target_group_names = (target_group_names & MIRROR_GROUPS) | (
                current_group_names - MIRROR_GROUPS
            )

        if target_group_names != current_group_names:
            existing_groups = list(
                UserGroup.objects.filter(name__in=target_group_names).iterator()
            )
            existing_group_names = frozenset(group.name for group in existing_groups)

            new_groups = [
                UserGroup.objects.get_or_create(name=name,comment="Create groups from LDAP",created_by="System")[0]
                for name in target_group_names
                if name not in existing_group_names
            ]
            self._user.groups.set(existing_groups + new_groups)

