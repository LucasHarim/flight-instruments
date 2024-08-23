
from distutils.core import setup

setup(name='flight-instruments',
      version='1.0',
      description='Flight instruments for general purpose',
      author='Lucas Harim G. C.',
      author_email='harimlgc@usp.br',
      packages = ['flight_instruments'],
    install_requires = [
      'pygame']
     )