from django.utils.translation import ugettext_lazy as _
from django.db import models

from .validatiors import AminoAcidValidator


class AminoAcidSequenceField(models.CharField):
    description = _("Amino acid sequence (up to %(max_length)s)")

    def __init__(self, *args, **kwargs):
        super(AminoAcidSequenceField, self).__init__(*args, **kwargs)
        self.validators.append(AminoAcidValidator)
