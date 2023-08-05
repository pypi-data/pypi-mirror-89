import logging

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

from ...core.apps.users.models import DjangoSsoAppUserModelMixin

logger = logging.getLogger('django_sso_app.backend.users')


class User(AbstractUser, DjangoSsoAppUserModelMixin):

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})
