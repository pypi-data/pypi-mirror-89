from django.apps import AppConfig


class DjangeloAppConfig(AppConfig):
    name         = 'djangelo'
    verbose_name = 'Django ELO rating plugin'

    class DjangeloMeta:
        name = 'Django ELO rating plugin'

    def ready(self):
        from . import signals  # noqa
