from django.core.validators import RegexValidator

AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'

AminoAcidValidator = RegexValidator(r'^[%s]*$' % AMINO_ACIDS,
                                    'Only uppercase amino acid abbreviations are allowed.')

AminoAcidAlignmentValidator = RegexValidator(r'^[%s\-]*$' % AMINO_ACIDS,
                                             'Only uppercase amino acid abbreviations or dashes are allowed.')
