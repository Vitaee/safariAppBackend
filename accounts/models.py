from django.db import models
from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from safari.models import Safari

class User(AbstractBaseUser):
    username = models.CharField(
        verbose_name=_('username'),
        max_length=40,
        unique=True,
    )
    email = models.EmailField(verbose_name=_('email'), max_length=90, null=True)
    profile_image = models.TextField(verbose_name=_('profile image'), null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    objects = UserManager()
    USERNAME_FIELD = 'username'

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Favorites(models.Model):
    """
    This model holds users fav safari trips
    """
    user =  models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="User")
    safari = models.ForeignKey(Safari, on_delete=models.CASCADE, verbose_name="Safari Tour")
