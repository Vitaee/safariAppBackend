from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class SafariConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "safari"
    verbose_name = _('safari')
