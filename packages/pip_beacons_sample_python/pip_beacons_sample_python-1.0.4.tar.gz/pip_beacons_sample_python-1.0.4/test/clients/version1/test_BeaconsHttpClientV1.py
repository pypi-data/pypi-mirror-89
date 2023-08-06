# -*- coding: utf-8 -*-
"""
    step8.test.TestBeaconsHttpClientV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TestBeaconsHttpClientV1 class

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import time

from pip_services3_commons.config import ConfigParams
from pip_services3_commons.refer import References, Descriptor

from pip_beacons_sample_python.clients.version1.BeaconsHttpClientV1 import BeaconsHttpClientV1
from pip_beacons_sample_python.logic.BeaconsController import BeaconsController
from pip_beacons_sample_python.persistence.BeaconsMemoryPersistence import BeaconsMemoryPersistence
from pip_beacons_sample_python.services.version1.BeaconsHttpServiceV1 import BeaconsHttpServiceV1
from test.clients.version1.BeaconsClientV1Fixture import BeaconsClientV1Fixture

http_config = ConfigParams.from_tuples(
            'connection.protocol', 'http',
            'connection.port', 3000,
            'connection.host', 'localhost')

class TestBeaconsHttpClientV1():
    @classmethod
    def setup_class(cls):
        cls.controller = BeaconsController()
        cls.persistence = BeaconsMemoryPersistence()

        cls.service = BeaconsHttpServiceV1()
        cls.service.configure(http_config)

        cls.client = BeaconsHttpClientV1()
        cls.client.configure(http_config)

        cls.references = References.from_tuples(
            Descriptor('beacons', 'persistence', 'memory', 'default', '1.0'), cls.persistence,
            Descriptor('beacons', 'controller', 'default', 'default', '1.0'), cls.controller,
            Descriptor('beacons', 'service', 'http', 'default', '1.0'), cls.service,
            Descriptor('beacons', 'client', 'http', 'default', '1.0'), cls.client
        )
        cls.controller.set_references(cls.references)
        cls.client.set_references(cls.references)
        cls.service.set_references(cls.references)

        cls.fixture = BeaconsClientV1Fixture(cls.client)

        #cls.persistence.open(None)
        cls.service.open(None)
        cls.client.open(None)

    def teardown_method(self, method):
        self.client.close(None)
        self.service.close(None)
        #self.persistence.close(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()
        pass

    # def test_calculate_position(self):
    #     self.fixture.test_calculate_position()