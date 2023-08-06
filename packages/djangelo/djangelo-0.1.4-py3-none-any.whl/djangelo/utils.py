from django.contrib.contenttypes.models import ContentType

from djangelo.models import ELORated


class EloDescriptor:

    def __get__(self, obj, objtype=None):
        return ELORated.objects.get(
            content_type = ContentType.objects.get_for_model(obj),
            object_id    = obj.id
        )

    def __set__(self, *args, **kwargs):
        raise AttributeError('READ ONLY')
