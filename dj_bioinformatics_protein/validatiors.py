from django.core.validators import RegexValidator

AMINO_ACIDS = 'ACDEFGHIKLMNPQRSTVWY'
WILDCARD = 'X'

AminoAcidValidator = RegexValidator(
    r'^[%s]*$' % AMINO_ACIDS,
    'Only uppercase amino acid abbreviations are allowed.'
)

AminoAcidWithNonCanonicalValidator = RegexValidator(
    r'^[%s]*$' % (AMINO_ACIDS + WILDCARD),
    'Only uppercase amino acid abbreviations are allowed, or X (non canonical residues).'
)

AminoAcidAlignmentValidator = RegexValidator(
    r'^[%s\-]*$' % AMINO_ACIDS,
    'Only uppercase amino acid abbreviations or dashes are allowed.'
)

AminoAcidWithNonCanonicalAlignmentValidator = RegexValidator(
    r'^[%s\-]*$' % (AMINO_ACIDS + WILDCARD),
    'Only uppercase amino acid abbreviations or dashes are allowed, or X (non canonical residues).'
)
