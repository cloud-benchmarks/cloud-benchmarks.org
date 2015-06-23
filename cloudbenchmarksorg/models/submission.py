import logging

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

    @property
    def result(self):
        return self.data['action']['output']['meta']['composite']

    @property
    def services_dict(self):
        """Return the 'services' dict from this submission's bundle.

        """
        return self.data['bundle']['services']

    def services(self, filtered=False):
        for s in self.services_dict.values():
            c = Service(s)
            if filtered and c.charm_name in FILTERED_CHARMS:
                continue
            yield Service(s)

    @property
    def svg(self):
        """Return svg data for this Submission's bundle.

        """
        if self._svg:
            return self._svg

        r = requests.post(
            SVG_URL,
            yaml.safe_dump(
                dict(bundle=self.data['bundle']),
                default_flow_style=False))
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
