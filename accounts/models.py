# coding: utf-8
from __future__ import unicode_literals

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import UserManager
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from filer.fields.image import FilerImageField

from . import choices


class BaseUserManager(UserManager):
    def _create_user(   self, username, password,
                        is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        if not username:
            raise ValueError('The given username must be set')
        username = self.normalize_email(username)
        user = self.model(username=username, is_staff=is_staff, is_active=True,
                    is_superuser=is_superuser, date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, password, False, False,
                                **extra_fields)

    def create_superuser(self, username, password, **extra_fields):
        return self._create_user(username, password, True, True,
                                **extra_fields)


class AbstractUser(AbstractBaseUser, PermissionsMixin):
    username = models.EmailField(_('username'), max_length=255, unique=True,
        error_messages={
                    'unique': _("A user with that username already exists."),
    })
    is_staff = models.BooleanField(_('staff status'), default=False,
            help_text=_('Designates whether the user can log into this admin '
                'site.'))
    is_active = models.BooleanField(_('active'), default=True,
            help_text=_('Designates whether this user should be treated as '
                'active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    objects = BaseUserManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ()

    @property
    def email(self):
        return self.username

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def get_full_name(self):
        return self.fio.strip()
    
    def get_short_name(self):
        return self.fio
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):
    fio = models.CharField(_('Full name'), max_length=1024, blank=True)
    version = models.CharField(
        _('Account version'), max_length=8, default='CLASSIC',
        choices=choices.ACCOUNT_VERSIONS)
    avatar = FilerImageField(verbose_name=_('Avatar'), null=True, blank=True)

    __unicode__ = lambda self: self.username

    class Meta:
        ordering = '-id', '-date_joined',
        verbose_name=_('User')
        verbose_name_plural=_('Users')

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)

    @property
    def email(self):
        return self.username
