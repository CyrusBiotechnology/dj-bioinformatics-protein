import logging
import hashlib
import os
import re

from django.db import models
from django.conf import settings

from dj_bioinformatics_protein.validatiors import AminoAcidWithNonCanonicalValidator, \
    AminoAcidWithNonCanonicalAlignmentValidator
from .fields import AminoAcidSequenceField, AminoAcidAlignmentField

logger = logging.getLogger('dj_bioinformatics_protein.' + __name__)

FORMATS_SETTINGS = {
    "MAX_DESCRIPTION_LENGTH": 1000,
    "MAX_SEQUENCE_LENGTH": 5000,
    "ALIGNMENT": {
        'PDB_CODE_LENGTH': 4,
        'PDB_CHAIN_LENGTH': 1,
    }
}

try:
    FORMATS_SETTINGS.update(settings.FORMATS)
except AttributeError:
    pass


class FASTA(models.Model):
    """ To the client, this is usually represented with the __str__ method; the entire
    file. However, there are lots of advantages to storing the FASTA file as 4 different
    fields in the database, or storing the sequence on disk and the remaining three in
    the database. Since the hash of the sequence should be unique, we can look up FASTAs
    either locally or on remote systems with this unique hash, to be sure we aren't
    storing two of the same sequence. This also allows us to do should also do some
    higher-level checks to make sure that that two jobs are not run with the same
    sequence against the same database. With deterministic applications, we will get the
    same result.
    """

    # SHA 256 hash is generated on the fly, to enforce uniqueness of sequence field
    sha256 = models.CharField(unique=True, editable=False, blank=True, max_length=255)

    # FASTA body fields
    description = models.CharField(max_length=FORMATS_SETTINGS['MAX_DESCRIPTION_LENGTH'])
    comments = models.TextField(null=True)
    sequence = AminoAcidSequenceField(
        validators=[AminoAcidWithNonCanonicalValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH']
    )

    def header(self, allow_comments=False):
        """ Generate the header string
        :param allow_comments: Choose to allow comments to be printed in the output
        :return: Properly formatted header string
        """
        if allow_comments and self.comments:
            header = ';' + str(self.description)
            header += os.linesep.join(['; ' + comment for comment in self.comments.split('\n')])
        else:
            header = '>' + str(self.description)
        return header

    def body(self, line_length=80):
        """ Break the sequence in to lines of line_length
        :param line_length: int; break lines to this length
        :return: formatted body
        """
        sequence = str(self.sequence)
        parsed = [sequence[i:i + line_length] for i in range(0, len(sequence), line_length)]
        return os.linesep.join(parsed)

    @property
    def formatted(self):
        fasta = self.header()
        fasta += os.linesep
        fasta += self.body()
        return str(fasta)

    @property
    def hash(self):
        return hashlib.sha256(self.sequence).hexdigest()

    @staticmethod
    def clean_sequence(sequence):
        _sequence = ''.join(re.findall('(\w+)', sequence))
        return _sequence.upper()

    def save(self, *args, **kwargs):
        if not self.sha256:
            self.sha256 = self.hash
        self.description.strip()
        self.description.lstrip('>;')
        self.sequence = self.clean_sequence(self.sequence)
        super(FASTA, self).save(*args, **kwargs)

    @classmethod
    def from_fasta(cls, fasta):
        """ Builds a FASTA object from a FASTA file. We use this during deserialization
        of objects to turn the FASTA passed as a string into a FASTA instance in the db.

        PLEASE NOTE, this function doesn't persist FASTA objects! You must run .save()
        on instances returned by this function!

        :param fasta: FASTA file (entire file as a string with newlines)
        :return: a single populated FASTA object
        """

        fasta_object = cls()

        fasta_object.description = ''
        fasta_object.comments = ''
        fasta_object.sequence = ''

        split = []
        for l in [l for l in fasta.split('\\n')]:
            split += l.split('\n')

        for i, line in enumerate(split):
            _line = line.rstrip()

            if _line.startswith('>') and i == 0:
                fasta_object.description = _line[1:]
            elif _line.startswith(';') and i == 0:
                fasta_object.description = _line[1:]
            elif _line.startswith(';') and i != 1:
                fasta_object.comments += _line[1:] + '\n'
            else:
                fasta_object.sequence += _line

        if not fasta_object.sequence:
            raise Exception(("No FASTA sequence given. Make sure your FASTA is"
                             " formatted properly and try again"))

        return fasta_object

    def __str__(self):
        return str(self.formatted)

try:
    """ Maximum FASTA length is limited to the sum of all field limits by
    default, but this may be overridden by adding the following setting in
    settings.py:

    FORMATS = {
        'FASTA': {
            'MAX_FASTA_FILE_LENGTH': <integer>
        }
    }

    It's also possible to override the length of a single field (which will
    affect the total length automatically) by providing that field instead:

    FORMATS = {
        'FASTA': {
            'MAX_DESCRIPTION_LENGTH': 255,
            'MAX_COMMENTS_LENGTH': 2000,
            'MAX_SEQUENCE_LENGTH': 5000,
        }
    }

    """
    MAX_FASTA_FILE_LENGTH = settings.FORMATS['MAX_SEQUENCE_LENGTH']
except (AttributeError, IndexError, KeyError):
    """ Failing to get FASTA length from settings, we can infer the maximum
    FASTA length we should accept by summing the max_length of all the fields
    of the FASTA object. This is an imperfect solution, since we could
    potentially have a single field that is too long, but we assume we've
    chosen sane limits on our side. We also assume that the client app does
    some checking before sending data and is able to handle 4XX & 5XX errors in
    a sane way, notifying the end user. """
    MAX_FASTA_FILE_LENGTH = FASTA._meta.get_field('description').max_length
    try:
        MAX_FASTA_FILE_LENGTH += FASTA._meta.get_field('comments').max_length
    except TypeError:
        pass
    MAX_FASTA_FILE_LENGTH += FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH']


class Alignment(models.Model):
    """ Represents one alignment
    """

    JSON_FIELDS = [
        "alignment_method",
        "rank",
        "query_description",
        "target_description",
        "target_pdb_code",
        "target_pdb_chain",
        "query_start",
        "query_aln_seq",
        "target_start",
        "target_aln_seq",
        "score_line",
        "p_correct",
        "threaded_template"
    ]

    ALIGNMENT_SETTINGS = FORMATS_SETTINGS['ALIGNMENT']

    ALIGN_METHOD_CHOICES = [
        ('H', 'hhsearch'),
        ('S', 'sparksX'),
        ('U', 'user'),
    ]

    user_template = False  # search for pdb database or user defined files

    full_query_sequence = AminoAcidSequenceField(
        validators=[AminoAcidWithNonCanonicalValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH']
    )
    query_aln_seq = AminoAcidAlignmentField(
        validators=[AminoAcidWithNonCanonicalAlignmentValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH']
    )
    alignment_method = models.CharField(max_length=1, choices=ALIGN_METHOD_CHOICES)
    rank = models.IntegerField()
    active = models.BooleanField(default=True)

    # modeled sequence information
    query_start = models.IntegerField()  # 1 based
    query_description = models.CharField(max_length=FORMATS_SETTINGS['MAX_DESCRIPTION_LENGTH'], null=True)
    modified_query_aln_seq = AminoAcidAlignmentField(
        validators=[AminoAcidWithNonCanonicalAlignmentValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH'],
        null=True
    )

    # template information
    target_start = models.IntegerField()  # 1 based
    target_description = models.CharField(max_length=FORMATS_SETTINGS['MAX_DESCRIPTION_LENGTH'], null=True)
    target_pdb_code = models.CharField(max_length=ALIGNMENT_SETTINGS['PDB_CODE_LENGTH'])
    target_pdb_chain = models.CharField(max_length=ALIGNMENT_SETTINGS['PDB_CHAIN_LENGTH'])
    target_aln_seq = AminoAcidAlignmentField(
        validators=[AminoAcidWithNonCanonicalAlignmentValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH'])
    modified_target_aln_seq = AminoAcidAlignmentField(
        validators=[AminoAcidWithNonCanonicalAlignmentValidator],
        max_length=FORMATS_SETTINGS['MAX_SEQUENCE_LENGTH'],
        null=True
    )

    p_correct = models.FloatField()  # current using Robetta p_correct calculator. to be improved using alignment score

    threaded_template = models.TextField(blank=True, null=True)

    @property
    def target_grishin_tag(self):
        if self.alignment_method == 'H':
            tag = "%s%s_%3d" % (self.target_pdb_code, self.target_pdb_chain, self.rank + 200)
        elif self.alignment_method == 'S':
            tag = "%s%s_%3d" % (self.target_pdb_code, self.target_pdb_chain, self.rank + 300)
        else:
            tag = "%s%s_%3d" % (self.target_pdb_code, self.target_pdb_chain, self.rank + 400)
        return str(tag)

    @property
    def grishin_lines(self):
        outlines = "## %s %s\n" % (self.query_description, self.target_grishin_tag)
        outlines += "#  \n"
        outlines += "scores_from_program: 0\n"

        outlines += "%d %s\n" % (self.query_start - 1, self.query_aln_seq)
        outlines += "%d %s\n" % (self.target_start - 1, self.target_aln_seq)
        outlines += "--\n\n"
        return str(outlines)

    @property
    def hash(self):
        return hashlib.sha256(self.grishin_lines).hexdigest()

    def load_data(self, data_in):
        for attr in self.JSON_FIELDS:
            if attr in data_in.keys():
                if attr == 'alignment_method':
                    if data_in[attr] == "hhsearch":
                        self.alignment_method = 'H'
                    elif data_in[attr] == "sparksX":
                        self.alignment_method = 'S'
                    else:
                        logger.warning("Currently user input alignment not supported")
                        self.alignment_method = 'U'
                else:
                    self.__dict__[attr] = data_in[attr]

    def dump_data(self):
        aln = {}
        for attr in self.JSON_FIELDS:
            if attr not in self.__dict__.keys():
                logger.warning("Missing data for %s in the alignment." % attr)
            if attr in self.__dict__.keys() and self.__dict__[attr] is not None:
                if attr == "alignment_method":
                    if self.alignment_method == 'H':
                        aln[attr] = "hhsearch"
                    elif self.alignment_method == 'S':
                        aln[attr] = "sparksX"
                    else:
                        aln[attr] = "user"
                else:
                    aln[attr] = self.__dict__[attr]
        aln['FASTA'] = self.full_query_sequence.formatted
        aln['target_grishin_tag'] = self.target_grishin_tag
        aln['grishin_lines'] = self.grishin_lines
        return aln

    def __str__(self):
        return self.grishin_lines
