# coding: utf-8
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import redirect
from django.views.generic import DetailView, RedirectView, TemplateView
from django.utils.translation import ugettext_lazy as _
from django.template import loader

from ..mixins import LoginReqMixin, ProfileMixin
from ..serializers import EmailConfirmationSerializer


class RegistrationView(TemplateView):
    template_name = 'registration/registration_form.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect(reverse('accounts:profile-private'))
        return super(RegistrationView, self).get(request, *args, **kwargs)


class ProfileOptionsView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card.html'


class ProfileOffersView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card2.html'


class ProfileHistoryView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card3.html'


class ProfilePrivateView(LoginReqMixin, ProfileMixin, DetailView):
    template_name = 'accounts/profile/user-card4.html'


class EmailConfirmationView(RedirectView):
    permanent = False
    pattern_name = 'accounts:profile-private'

    def get(self, request, *args, **kwargs):
        serializer = EmailConfirmationSerializer(data=request.GET)
        if serializer.is_valid():
            serializer.save()
            user = serializer._get_user()
            template_name = 'accounts/email/email_confirmed.html'
            mail_kwargs = {
                'subject': _('Sportomatics: E-Mail confirmation'),
                'message': 'HTML',
                'from_email': 'no-reply@sportomatics.ru',
                'recipient_list': [user.username],
                'html_message': loader.render_to_string(template_name, {}),
            }
            from django.core.mail import send_mail
            send_mail(**mail_kwargs)
            return super(EmailConfirmationView, self).get(
                request, *args, **kwargs)
        else:
            raise Http404
