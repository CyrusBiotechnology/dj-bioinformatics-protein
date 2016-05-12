from setuptools import setup

setup(name='dj_bioinformatics_protein',
      version='1.0.5',
      description='Django utilities and tools for protein storage and manipulation',
      url='http://github.com/CyrusBiotechnology/dj-protein',
      author='Peter Novotnak, Yifan Song',
      author_email='peter@cyrusbio.com, yifan@cyrusbio.com',
      license='MIT',
      packages=['dj_bioinformatics_protein', 'dj_bioinformatics_protein.migrations'],
      zip_safe=True)
