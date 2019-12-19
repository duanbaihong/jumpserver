# -*- coding: utf-8 -*-
#

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db import transaction
from django.utils import timezone
from rest_framework.renderers import JSONRenderer
from rest_framework.request import Request

from jumpserver.utils import current_request
from common.utils import get_request_ip, get_logger, get_syslogger
from users.models import User
from authentication.signals import post_auth_failed, post_auth_success
from terminal.models import Session, Command
from terminal.backends.command.serializers import SessionCommandSerializer
from . import models, serializers
from .tasks import write_login_log_async

logger = get_logger(__name__)
sys_logger = get_syslogger("audits")
json_render = JSONRenderer()


MODELS_NEED_RECORD = (
    'User', 'UserGroup', 'Asset', 'Node', 'AdminUser', 'SystemUser',
    'Domain', 'Gateway', 'Organization', 'AssetPermission', 'CommandFilter',
    'CommandFilterRule', 'License', 'Setting', 'Account', 'SyncInstanceTask',
)


def create_operate_log(action, sender, resource):
    user = current_request.user if current_request else None
    if not user or not user.is_authenticated:
        return
    model_name = sender._meta.object_name
    if model_name not in MODELS_NEED_RECORD:
        return
    resource_type = sender._meta.verbose_name
    remote_addr = get_request_ip(current_request)

    data = {
        "user": str(user), 'action': action, 'resource_type': resource_type,
        'resource': str(resource), 'remote_addr': remote_addr,
    }
    with transaction.atomic():
        try:
            models.OperateLog.objects.create(**data)
        except Exception as e:
            logger.error("Create operate log error: {}".format(e))


@receiver(post_save, dispatch_uid="my_unique_identifier")
def on_object_created_or_update(sender, instance=None, created=False, **kwargs):
    if created:
        action = models.OperateLog.ACTION_CREATE
    else:
        action = models.OperateLog.ACTION_UPDATE
    create_operate_log(action, sender, instance)


@receiver(post_delete, dispatch_uid="my_unique_identifier")
def on_object_delete(sender, instance=None, **kwargs):
    create_operate_log(models.OperateLog.ACTION_DELETE, sender, instance)


@receiver(post_save, sender=User, dispatch_uid="my_unique_identifier")
def on_user_change_password(sender, instance=None, **kwargs):
    if hasattr(instance, '_set_password'):
        if not current_request or not current_request.user.is_authenticated:
            return
        with transaction.atomic():
            models.PasswordChangeLog.objects.create(
                user=instance, change_by=current_request.user,
                remote_addr=get_request_ip(current_request),
            )


def on_audits_log_create(sender, instance=None, **kwargs):
    if sender == models.UserLoginLog:
        category = "login_log"
        serializer = serializers.LoginLogSerializer
    elif sender == models.FTPLog:
        serializer = serializers.FTPLogSerializer
        category = "ftp_log"
    elif sender == models.OperateLog:
        category = "operation_log"
        serializer = serializers.OperateLogSerializer
    elif sender == models.PasswordChangeLog:
        category = "password_change_log"
        serializer = serializers.PasswordChangeLogSerializer
    elif sender == Session:
        category = "host_session_log"
        serializer = serializers.SessionAuditSerializer
    elif sender == Command:
        category = "session_command_log"
        serializer = SessionCommandSerializer
    else:
        return

    s = serializer(instance=instance)
    data = json_render.render(s.data).decode(errors='ignore')
    msg = "{} - {}".format(category, data)
    sys_logger.info(msg)


def generate_data(username, request):
    user_agent = request.META.get('HTTP_USER_AGENT', '')

    if isinstance(request, Request):
        login_ip = request.data.get('remote_addr', '0.0.0.0')
        login_type = request.data.get('login_type', '')
    else:
        login_ip = get_request_ip(request) or '0.0.0.0'
        login_type = 'W'

    data = {
        'username': username,
        'ip': login_ip,
        'type': login_type,
        'user_agent': user_agent,
        'datetime': timezone.now()
    }
    return data


@receiver(post_auth_success)
def on_user_auth_success(sender, user, request, **kwargs):
    logger.debug('User login success: {}'.format(user.username))
    data = generate_data(user.username, request)
    data.update({'mfa': int(user.mfa_enabled), 'status': True})
    write_login_log_async.delay(**data)


@receiver(post_auth_failed)
def on_user_auth_failed(sender, username, request, reason, **kwargs):
    logger.debug('User login failed: {}'.format(username))
    data = generate_data(username, request)
    data.update({'reason': reason, 'status': False})
    write_login_log_async.delay(**data)
