from django.core.validators import RegexValidator

AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'

AminoAcidValidator = RegexValidator(r'^[%s]*$' % AMINO_ACIDS,
                                    'Only uppercase alphanumeric characters are allowed.')
