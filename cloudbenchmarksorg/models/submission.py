import logging

from cached_property import cached_property
import requests
import yaml

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
)

from .base import Base


log = logging.getLogger(__name__)

SVG_URL = 'http://svg.juju.solutions'
FILTERED_CHARMS = (
    'collectd', 'cabs', 'cabs-collector',
    'benchmark-gui', 'siege',
)


class Submission(Base):
    environment_id = Column(Integer, ForeignKey('environment.id'))

    data = Column(JSONB)
    _svg = Column(String)
    _service_names = Column(JSONB)
    environment = relationship('Environment')

    def __init__(self, *args, **kw):
        super(Submission, self).__init__(*args, **kw)
        # Store parsed service names in a json column
        # so we can query against it later
        self._service_names = [s.charm_name for s in self.services()]

    @cached_property
    def bundle(self):
        """Return bundle for this Submission, as a dict.

        """
        return dict(bundle=self.data['bundle'])

    @cached_property
    def bundle_yaml(self):
        """Return bundle for this Submission, as yaml.

        """
        return yaml.safe_dump(self.bundle, default_flow_style=False)

    @property
    def result(self):
        return self.data['action']['output']['meta']['composite']

    def services(self, filtered=False):
        """Yield a Service object for each service in self.bundle

        """
        for s in self.bundle['bundle']['services'].values():
            c = Service(s)
            if filtered and c.charm_name in FILTERED_CHARMS:
                continue
            yield Service(s)

    @property
    def svg(self):
        """Return svg data for self.bundle

        """
        if self._svg:
            return self._svg

        r = requests.post(SVG_URL, self.bundle_yaml)
        try:
            r.raise_for_status()
        except Exception as e:
            log.exception(e)
            return None

        self._svg = r.content.decode('utf-8')
        return self._svg


class Service(object):
    def __init__(self, data):
        self.data = data
        self.charm_name = self._parse_name()
        self.unit_count = self._parse_count()

    def _parse_name(self):
        charm = self.data['charm']
        _, charm = charm.rsplit('/', 1)
        charm, _ = charm.rsplit('-', 1)
        return charm

    def _parse_count(self):
        num_units = self.data['num_units']
        return int(num_units)
