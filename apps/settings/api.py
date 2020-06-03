# -*- coding: utf-8 -*-
#

import json

from smtplib import SMTPSenderRefused
from rest_framework import generics
from rest_framework.views import Response, APIView
from django.conf import settings
from django.core.mail import send_mail, get_connection
from django.utils.translation import ugettext_lazy as _

from .utils import (
    LDAPServerUtil, LDAPCacheUtil, LDAPImportUtil, LDAPSyncUtil,
    LDAP_USE_CACHE_FLAGS, LDAPTestUtil,
)
from .tasks import sync_ldap_user_task
from common.permissions import IsOrgAdmin, IsSuperUser
from common.utils import get_logger
from .serializers import (
    MailTestSerializer, LDAPTestConfigSerializer, LDAPUserSerializer,
    PublicSettingSerializer, LDAPTestLoginSerializer,LDAPTestUserSerializer
)
from users.models import User
from authentication.backends.ldap import LDAPAuthorizationBackend

logger = get_logger(__file__)


class MailTestingAPI(APIView):
    permission_classes = (IsSuperUser,)
    serializer_class = MailTestSerializer
    success_message = _("Test mail sent to {}, please check")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            email_host = serializer.validated_data['EMAIL_HOST']
            email_port = serializer.validated_data['EMAIL_PORT']
            email_host_user = serializer.validated_data["EMAIL_HOST_USER"]
            email_host_password = serializer.validated_data['EMAIL_HOST_PASSWORD']
            email_from = serializer.validated_data["EMAIL_FROM"]
            email_recipient = serializer.validated_data["EMAIL_RECIPIENT"]
            email_use_ssl = serializer.validated_data['EMAIL_USE_SSL']
            email_use_tls = serializer.validated_data['EMAIL_USE_TLS']

            # 设置 settings 的值，会导致动态配置在当前进程失效
            # for k, v in serializer.validated_data.items():
            #     if k.startswith('EMAIL'):
            #         setattr(settings, k, v)
            try:
                subject = "Test"
                message = "Test smtp setting"
                email_from = email_from or email_host_user
                email_recipient = email_recipient or email_from
                connection = get_connection(
                    host=email_host, port=email_port,
                    uesrname=email_host_user, password=email_host_password,
                    use_tls=email_use_tls, use_ssl=email_use_ssl,
                )
                send_mail(
                    subject, message,  email_from, [email_recipient],
                    connection=connection
                )
            except SMTPSenderRefused as e:
                resp = e.smtp_error
                if isinstance(resp, bytes):
                    for coding in ('gbk', 'utf8'):
                        try:
                            resp = resp.decode(coding)
                        except UnicodeDecodeError:
                            continue
                        else:
                            break
                return Response({"error": str(resp)}, status=401)
            except Exception as e:
                print(e)
                return Response({"error": str(e)}, status=401)
            return Response({"msg": self.success_message.format(email_recipient)})
        else:
            return Response({"error": str(serializer.errors)}, status=401)


class LDAPTestingConfigAPI(APIView):
    permission_classes = (IsSuperUser,)
    serializer_class = LDAPTestConfigSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"error": str(serializer.errors)}, status=401)
        config = self.get_ldap_config(serializer)
        ok, msg = LDAPTestUtil(config).test_config()
        status = 200 if ok else 401
        return Response(msg, status=status)

    @staticmethod
    def get_ldap_config(serializer):
        server_uri = serializer.validated_data["AUTH_LDAP_SERVER_URI"]
        bind_dn = serializer.validated_data["AUTH_LDAP_BIND_DN"]
        password = serializer.validated_data["AUTH_LDAP_BIND_PASSWORD"]
        use_ssl = serializer.validated_data.get("AUTH_LDAP_START_TLS", False)
        search_ou = serializer.validated_data["AUTH_LDAP_SEARCH_OU"]
        search_filter = serializer.validated_data["AUTH_LDAP_SEARCH_FILTER"]
        attr_map = serializer.validated_data["AUTH_LDAP_USER_ATTR_MAP"]
        auth_ldap = serializer.validated_data.get('AUTH_LDAP', False)
        config = {
            'server_uri': server_uri,
            'bind_dn': bind_dn,
            'password': password,
            'use_ssl': use_ssl,
            'search_ou': search_ou,
            'search_filter': search_filter,
            'attr_map': attr_map,
            'auth_ldap': auth_ldap
        }
        return config


class LDAPTestingLoginAPI(APIView):
    permission_classes = (IsSuperUser,)
    serializer_class = LDAPTestLoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if not serializer.is_valid():
            return Response({"error": str(serializer.errors)}, status=401)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        ok, msg = LDAPTestUtil().test_login(username, password)
        status = 200 if ok else 401
        return Response(msg, status=status)


class LDAPUserListApi(generics.ListAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = LDAPUserSerializer

    def get_queryset_from_cache(self):
        search_value = self.request.query_params.get('search')
        users = LDAPCacheUtil().search(search_value=search_value)
        return users

    def get_queryset_from_server(self):
        search_value = self.request.query_params.get('search')
        users = LDAPServerUtil().search(search_value=search_value)
        return users

    def get_queryset(self):
        if hasattr(self, 'swagger_fake_view'):
            return []
        cache_police = self.request.query_params.get('cache_police', True)
        if cache_police in LDAP_USE_CACHE_FLAGS:
            users = self.get_queryset_from_cache()
        else:
            users = self.get_queryset_from_server()
        return users

    @staticmethod
    def processing_queryset(queryset):
        db_username_list = User.objects.all().values_list('username', flat=True)
        for q in queryset:
            q['id'] = q['username']
            q['existing'] = q['username'] in db_username_list
        return queryset

    def sort_queryset(self, queryset):
        order_by = self.request.query_params.get('order')
        if not order_by:
            order_by = 'existing'
        if order_by.startswith('-'):
            order_by = order_by.lstrip('-')
            reverse = True
        else:
            reverse = False
        queryset = sorted(queryset, key=lambda x: x[order_by], reverse=reverse)
        return queryset

    def filter_queryset(self, queryset):
        if queryset is None:
            return queryset
        queryset = self.processing_queryset(queryset)
        queryset = self.sort_queryset(queryset)
        return queryset

    def list(self, request, *args, **kwargs):
        cache_police = self.request.query_params.get('cache_police', True)
        # 不是用缓存
        if cache_police not in LDAP_USE_CACHE_FLAGS:
            return super().list(request, *args, **kwargs)

        try:
            queryset = self.get_queryset()
        except Exception as e:
            data = {'error': str(e)}
            return Response(data=data, status=400)

        # 缓存有数据
        if queryset is not None:
            return super().list(request, *args, **kwargs)

        sync_util = LDAPSyncUtil()
        # 还没有同步任务
        if sync_util.task_no_start:
            # 任务外部设置 task running 状态
            sync_util.set_task_status(sync_util.TASK_STATUS_IS_RUNNING)
            task = sync_ldap_user_task.delay()
            data = {'msg': 'Cache no data, sync task {} started.'.format(task.id)}
            return Response(data=data, status=409)
        # 同步任务正在执行
        if sync_util.task_is_running:
            data = {'msg': 'synchronization is running.'}
            return Response(data=data, status=409)
        # 同步任务执行结束
        if sync_util.task_is_over:
            msg = sync_util.get_task_error_msg()
            data = {'error': 'Synchronization task report error: {}'.format(msg)}
            return Response(data=data, status=400)

        return super().list(request, *args, **kwargs)


class LDAPUserImportAPI(APIView):
    permission_classes = (IsSuperUser,)

    def get_ldap_users(self):
        username_list = self.request.data.get('username_list', [])
        cache_police = self.request.query_params.get('cache_police', True)
        if cache_police in LDAP_USE_CACHE_FLAGS:
            users = LDAPCacheUtil().search(search_users=username_list)
        else:
            users = LDAPServerUtil().search(search_users=username_list)
        return users

    def post(self, request):
        try:
            users = self.get_ldap_users()
        except Exception as e:
            return Response({'error': str(e)}, status=401)

        if users is None:
            return Response({'msg': _('Get ldap users is None')}, status=401)

        errors = LDAPImportUtil().perform_import(users)
        if errors:
            return Response({'errors': errors}, status=401)

        count = users if users is None else len(users)
        return Response({'msg': _('Imported {} users successfully').format(count)})


class LDAPCacheRefreshAPI(generics.RetrieveAPIView):
    permission_classes = (IsSuperUser,)

    def retrieve(self, request, *args, **kwargs):
        try:
            LDAPSyncUtil().clear_cache()
        except Exception as e:
            logger.error(str(e))
            return Response(data={'msg': str(e)}, status=400)
        return Response(data={'msg': 'success'})


class PublicSettingApi(generics.RetrieveAPIView):
    permission_classes = ()
    serializer_class = PublicSettingSerializer

    def get_object(self):
        instance = {
            "data": {
                "WINDOWS_SKIP_ALL_MANUAL_PASSWORD": settings.WINDOWS_SKIP_ALL_MANUAL_PASSWORD,
                "SECURITY_MAX_IDLE_TIME": settings.SECURITY_MAX_IDLE_TIME,
            }
        }
        return instance

class LDAPTestingAPI(APIView):
    permission_classes = (IsOrgAdmin,)
    serializer_class = LDAPTestUserSerializer
    success_message = _("Test ldap success")

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            ldap_username = serializer.validated_data["AUTH_LDAP_USER_NAME"]
            ldap_password = serializer.validated_data["AUTH_LDAP_USERNAME_PASSWORD"]
            local_user=User.objects.filter(username=ldap_username,source='local')
            if local_user:
                 return Response({"error":_('The current user [{}] is a local user and can not perform LDAP authentication login test!').format(ldap_username)},status=401)
            users=LDAPAuthorizationBackend().authenticate(username=ldap_username,password=ldap_password)
            if users != None:
                return Response({"msg": _("Match users %(name)s(%(username)s),Groups [%(groups)s].")%({
                    'name': users.name,
                    'username': users.username,
                    'groups': users.groups_display})
                })
            else:
                return Response({"error": _("LDAP User {} Authentication Failed, Make sure the username or password is correct, or there are no find users").format(ldap_username)}, status=401)
        else:
            return Response({"error": serializer.errors}, status=401)
