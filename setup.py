from setuptools import setup

setup(name='spamexperts',
      version='0.0.1',
      description='A Python interface to the SpamExperts API',
      url='https://github.com/sensson/python-spamexperts',
      author='Sensson',
      author_email='info@sensson.net',
      packages=['spamexperts'],
      install_requires=[
          'requests',
      ],
      zip_safe=False)
