from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ProfilesConfig(AppConfig):
    name = 'lakodex_api.apps.profiles'
    verbose_name = _('profiles')

    def ready(self):
        import lakodex_api.apps.profiles.signals  # noqa
