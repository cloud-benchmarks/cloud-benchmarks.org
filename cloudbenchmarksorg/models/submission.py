import logging

import arrow
from cached_property import cached_property
import requests
import yaml

from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    Float,
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
    _result_value = Column(Float)
    _svg = Column(String)
    _service_names = Column(JSONB)
    benchmark_name = Column(String)
    environment = relationship('Environment')

    def __init__(self, *args, **kw):
        super(Submission, self).__init__(*args, **kw)
        # Store parsed service names in a json column
        # so we can query against it later
        try:
            self._result_value = float(self.result['value'])
        except ValueError:
            pass
        self._service_names = [s.charm_name for s in self.services().values()]
        self.benchmark_name = self._parse_benchmark_name()

    def _parse_benchmark_name(self):
        action = self.data['action']['action']
        receiver = action['receiver']
        action_name = action['name']
        service_name = '-'.join(receiver.split('-')[1:-1])
        charm_name = self.services()[service_name].charm_name
        return '{}:{}'.format(charm_name, action_name)

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

    @cached_property
    def human_created_at(self):
        return arrow.get(self.created_at).humanize()

    @property
    def parameters(self):
        return self.data['action']['action']['parameters']

    @property
    def result(self):
        output = self.data['action']['output']
        if 'meta' in output:
            return output['meta']['composite']
        return dict(value='')

    @property
    def results(self):
        return self.data['action']['output']['results']

    def services(self, filtered=False):
        """Yield a dict of service_name:Service for each service in self.bundle

        """
        d = {}
        for name, data in self.bundle['bundle']['services'].items():
            s = Service(data)
            if filtered and s.charm_name in FILTERED_CHARMS:
                continue
            d[name] = s
        return d

    @cached_property
    def summary(self):
        action = self.data['action']
        d = {
            'environment': self.environment.name,
            'result': self.result,
        }
        d.update({
            k: action[k]
            for k in ('status', 'started', 'completed')
        })
        d.update({
            k: action['action'][k]
            for k in ('tag', 'name', 'receiver')
        })
        return d

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
