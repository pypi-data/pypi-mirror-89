from django.conf import settings


class DjangoSettings():

    """Store the default setting value and lookup for the custom one"""

    @property
    def sensibility(self):
        return getattr(settings, 'SENSIBILITY', 32)

    @property
    def initial_value(self):
        return getattr(settings, 'INITIAL_VALUE', 1200)

    def settings_ready(self):
        if not hasattr(settings, 'DJANGELO'):
            print('djangelo not found')
            return False
        elif not settings.DJANGELO.get('RATED_MODELS', False):
            print('rated models not found')
            return False
        else:
            return True

    def get_rated_models(self):
        if self.settings_ready():
            return self.get_model_names_from_settings()

    def get_model_names_from_settings(self):
        models = settings.DJANGELO.get('RATED_MODELS')
        models = list(map(lambda string: string.lower(), models))
        models = list(map(lambda string: string.split('.')[1], models))
        return models
