from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils.translation import ugettext as _

from common.permissions import PermissionsMixin, IsSuperUser
from common import utils
from .utils import LDAPSyncUtil
from .forms import EmailSettingForm, LDAPSettingForm, BasicSettingForm, \
    TerminalSettingForm, SecuritySettingForm, EmailContentSettingForm, \
    LDAPTestforUsername


class BasicSettingView(PermissionsMixin, TemplateView):
    form_class = BasicSettingForm
    template_name = "settings/basic_setting.html"
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Basic setting'),
            'form': self.form_class(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            return redirect('settings:basic-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)


class EmailSettingView(PermissionsMixin, TemplateView):
    form_class = EmailSettingForm
    template_name = "settings/email_setting.html"
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Email setting'),
            'form': self.form_class(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            return redirect('settings:email-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)


class LDAPSettingView(PermissionsMixin, TemplateView):
    form_class = LDAPSettingForm
    form_user_class = LDAPTestforUsername
    template_name = "settings/ldap_setting.html"
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('LDAP setting'),
            'form': self.form_class(),
            'form_user': self.form_user_class(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            LDAPSyncUtil().clear_cache()
            return redirect('settings:ldap-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)


class TerminalSettingView(PermissionsMixin, TemplateView):
    form_class = TerminalSettingForm
    template_name = "settings/terminal_setting.html"
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        command_storage = utils.get_command_storage_setting()
        replay_storage = utils.get_replay_storage_setting()

        context = {
            'app': _('Settings'),
            'action': _('Terminal setting'),
            'form': self.form_class(),
            'replay_storage': replay_storage,
            'command_storage': command_storage
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            return redirect('settings:terminal-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)


class ReplayStorageCreateView(PermissionsMixin, TemplateView):
    template_name = 'settings/replay_storage_create.html'
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Create replay storage')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class CommandStorageCreateView(PermissionsMixin, TemplateView):
    template_name = 'settings/command_storage_create.html'
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Create command storage')
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)


class SecuritySettingView(PermissionsMixin, TemplateView):
    form_class = SecuritySettingForm
    template_name = "settings/security_setting.html"
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Security setting'),
            'form': self.form_class(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            return redirect('settings:security-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)


class EmailContentSettingView(PermissionsMixin, TemplateView):
    template_name = "settings/email_content_setting.html"
    form_class = EmailContentSettingForm
    permission_classes = [IsSuperUser]

    def get_context_data(self, **kwargs):
        context = {
            'app': _('Settings'),
            'action': _('Email content setting'),
            'form': self.form_class(),
        }
        kwargs.update(context)
        return super().get_context_data(**kwargs)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            msg = _("Update setting successfully")
            messages.success(request, msg)
            return redirect('settings:email-content-setting')
        else:
            context = self.get_context_data()
            context.update({"form": form})
            return render(request, self.template_name, context)
