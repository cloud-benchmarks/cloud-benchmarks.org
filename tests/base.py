import json
import os
import unittest

from pyramid import testing
from paste.deploy.loadwsgi import appconfig
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker
from webtest import TestApp

from cloudbenchmarksorg import main
from cloudbenchmarksorg.models import DBSession
from cloudbenchmarksorg.models import Base  # base declarative object

here = os.path.dirname(__file__)
settings = appconfig('config:' + os.path.join(here, 'test.ini'))


class BaseTestCase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = engine_from_config(settings, prefix='sqlalchemy.')
        cls.Session = sessionmaker()

        # load submission data for use in tests
        here = os.path.dirname(os.path.abspath(__file__))
        with open(os.path.join(here, 'data', 'submission.json')) as f:
            cls.submission_data = json.load(f)

    def setUp(self):
        connection = self.engine.connect()

        # begin a non-ORM transaction
        self.trans = connection.begin()

        # bind an individual Session to the connection
        DBSession.configure(bind=connection)
        self.session = self.Session(bind=connection)
        Base.session = self.session

    def tearDown(self):
        # rollback - everything that happened with the
        # Session above (including calls to commit())
        # is rolled back.
        testing.tearDown()
        self.trans.rollback()
        self.session.close()


class UnitTestBase(BaseTestCase):
    def setUp(self):
        self.config = testing.setUp(request=testing.DummyRequest())
        super(UnitTestBase, self).setUp()


class IntegrationTestBase(BaseTestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = main({}, **settings)
        super(IntegrationTestBase, cls).setUpClass()

    def setUp(self):
        self.app = TestApp(self.app)
        self.config = testing.setUp()
        super(IntegrationTestBase, self).setUp()