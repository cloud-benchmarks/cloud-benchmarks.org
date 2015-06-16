import os

from setuptools import setup, find_packages

here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.md')) as f:
    README = f.read()
with open(os.path.join(here, 'CHANGES.txt')) as f:
    CHANGES = f.read()

requires = [
    'jsonschema',
    'pyramid',
    'pyramid_mako',
    'pyramid_debugtoolbar',
    'pyramid_tm',
    'SQLAlchemy',
    'transaction',
    'zope.sqlalchemy',
    'waitress',
    # test reqs
    'tox',
    ]

setup(name='cloud-benchmarks.org',
      version='0.0',
      description='cloud-benchmarks.org',
      long_description=README + '\n\n' + CHANGES,
      classifiers=[
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
        ],
      author='',
      author_email='',
      url='',
      keywords='web wsgi bfg pylons pyramid',
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False,
      test_suite='cloudbenchmarksorg',
      install_requires=requires,
      entry_points="""\
      [paste.app_factory]
      main = cloudbenchmarksorg:main
      [console_scripts]
      initialize_db = cloudbenchmarksorg.scripts.initializedb:main
      """,
      )
