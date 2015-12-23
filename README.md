# Formats Django App
This application is meant to be used behind the scenes, to provide data models that other
apps reference via FK relationships.

## Installing
Install this project as a submodule, or simply grab a snapshot of it from Github. Then
add it to your project as you would with any other app in your `INSTALLED_APPS` setting.

    INSTALLED_APPS = [
        ...
        'formats'
    ]

Then, migrate your database to create requisite tables.

## Using

### Models
All you need to do to use a format is reference it by PK!

```python
class AJob(models.Model):
    
    fasta_in = models.ForeignKey('formats.FASTA')
    
    ...the rest of your model's code
```

### DRF
In order to make `formats` convenient for you to use, a serializer and deserializer 
method to and from a string is provided for each model. This allows you to provide a 
single field on your serializer that represents a fully assembled file that is stored
as efficiently and with as little redundancy as possible in your database. 

To use a format in your `Serializer` class this way, override the FK field on your model 
with a plain `serializers.CharField`. It's maximum length should be set by 
`formats.models.formats.MAX_<type>_FILE_LENGTH` (eg; 
`formats.models.formats.MAX_FASTA_FILE_LENGTH`)
variable, which may be overridden in settings as desired.

```python
class AJobSerializer(serializers.HyperlinkedModelSerializer):

    """ Override fasta_in on FK with a charfield. During deserialization, we
    use this value to build a FASTA object and persist it to the DB, then pass 
    that persisted object to the 'AJob' we are creating. During serialization, 
    the serializer automatically pulls from __str__ on the related object, 
    which should be configured to return the formatted file. """
    fasta_in = serializers.CharField(max_length=MAX_FASTA_FILE_LENGTH)

    ...the rest of your serializer code
```

Then, override your `create`, `update`, etc. Methods to parse the FASTA string from the 
client. 
 
```python
def create(self, validated_data):
    """ During creation, you'll want to create your FASTA object in the DB and 
    update the model to point at it's PK
    """
    fasta = FASTA.from_fasta(validated_data.pop('fasta_in'))
    logger.debug("sequence is %s" % fasta.sequence)
    # Get or create fasta object
    try:
        fasta = FASTA.objects.get(sha256=fasta.hash)
    except FASTA.DoesNotExist:
        fasta.save()
    ...
```

As mentioned in the comments on the serializer field, serialization is handled 
automatically since the `__str__` method of the model returns a properly formatted FASTA 
file.

## TODO

 - Register this app on PyPi under Cyrus's account.
