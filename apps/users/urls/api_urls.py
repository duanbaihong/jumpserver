#!/usr/bin/env python
# ~*~ coding: utf-8 ~*~
#
from __future__ import absolute_import

from django.urls import path
from rest_framework_bulk.routes import BulkRouter

from authentication import api as auth_api
from .. import api

app_name = 'users'

router = BulkRouter()
router.register(r'users', api.UserViewSet, 'user')
router.register(r'groups', api.UserGroupViewSet, 'user-group')
router.register(r'users-groups-relations', api.UserUserGroupRelationViewSet, 'users-groups-relation')


urlpatterns = [
    path('connection-token/', auth_api.UserConnectionTokenApi.as_view(),
         name='connection-token'),
    path('profile/', api.UserProfileApi.as_view(), name='user-profile'),
    path('otp/reset/', api.UserResetOTPApi.as_view(), name='my-otp-reset'),
    path('users/<uuid:pk>/otp/reset/', api.UserResetOTPApi.as_view(), name='user-reset-otp'),
    path('users/<uuid:pk>/password/', api.UserChangePasswordApi.as_view(), name='change-user-password'),
    path('users/<uuid:pk>/password/reset/', api.UserResetPasswordApi.as_view(), name='user-reset-password'),
    path('users/<uuid:pk>/pubkey/reset/', api.UserResetPKApi.as_view(), name='user-public-key-reset'),
    path('users/<uuid:pk>/pubkey/update/', api.UserUpdatePKApi.as_view(), name='user-public-key-update'),
    path('users/<uuid:pk>/unblock/', api.UserUnblockPKApi.as_view(), name='user-unblock'),
]
urlpatterns += router.urls


