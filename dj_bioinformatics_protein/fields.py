from django.utils.translation import ugettext_lazy as _
from django.db import models

from .validatiors import AminoAcidValidator, AminoAcidAlignmentValidator


class AminoAcidSequenceField(models.CharField):
    default_validators = [AminoAcidValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidAlignmentField(models.CharField):
    default_validators = [AminoAcidAlignmentValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")
