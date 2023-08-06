from django.db import models
from django.db.models import Sum
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from ._elo_implementation import ELOComparator, ELOAlgorithmImplementation
from ._django_settings import DjangoSettings


class ELORated(ELOComparator, ELOAlgorithmImplementation, models.Model):

    """Defines the general behavior of an ELO rated object"""

    settings = DjangoSettings()

    value = models.IntegerField(editable=False, null=True)
    hints = models.IntegerField(editable=False, default=0)

    content_type   = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id      = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    def save(self, *args, **kwargs):
        self._set_default_value_on_creation()
        super(ELORated, self).save(*args, **kwargs)

    def _set_default_value_on_creation(self):
        if self.value is None:
            self.value = self.settings.initial_value

    @classmethod
    def _hints_sum(cls, queryset):
        return queryset.aggregate(Sum('hints'))['hints__sum']

    def get_global_hints_mean(self):
        allInstances      = ELORated.objects.all()
        allHintsSum       = self._hints_sum(allInstances)
        numberOfInstances = allInstances.count()
        return allHintsSum / numberOfInstances

    def up(self):
        self._update_value(1)

    def down(self):
        self._update_value(-1)

    def _update_value(self, addedValue):
        self.hints += addedValue
        self.save()
        super(ELORated, self).update_value(self.settings.sensibility)
        self.save()
