from django.utils.translation import ugettext_lazy as _
from django.db import models

from .validatiors import (
    AminoAcidWithNonCanonicalAlignmentValidator,
    AminoAcidWithNonCanonicalValidator,
)


class AminoAcidSequenceField(models.CharField):
    default_validators = [AminoAcidWithNonCanonicalValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")


class AminoAcidAlignmentField(models.CharField):
    default_validators = [AminoAcidWithNonCanonicalAlignmentValidator]
    description = _("Amino acid sequence (up to %(max_length)s)")
