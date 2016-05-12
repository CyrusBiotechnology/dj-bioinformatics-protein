from django.utils.translation import ugettext_lazy as _
from django.db import models

from .validatiors import AminoAcidValidator, AminoAcidAlignmentValidator


class AminoAcidSequenceCharField(models.CharField):
    default_validators = [AminoAcidValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidAlignmentCharField(models.CharField):
    default_validators = [AminoAcidAlignmentValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidSequenceTextField(models.CharField):
    default_validators = [AminoAcidValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidAlignmentTextField(models.TextField):
    default_validators = [AminoAcidAlignmentValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidAlignmentField(AminoAcidAlignmentCharField):
    pass


class AminoAcidSequenceField(AminoAcidAlignmentCharField):
    pass
