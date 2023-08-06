# -*- coding: utf-8 -*-
from pip_beacons_sample_python.clients.version1.BeaconsMockClientV1 import BeaconsMockClientV1
from .BeaconsClientV1Fixture import BeaconsClientV1Fixture

from pip_services3_commons.refer import References, Descriptor

from pip_beacons_sample_python.clients.version1.BeaconsDirectClientV1 import BeaconsDirectClientV1
from pip_beacons_sample_python.logic.BeaconsController import BeaconsController
from pip_beacons_sample_python.persistence.BeaconsMemoryPersistence import BeaconsMemoryPersistence
from test.clients.version1.BeaconsClientV1Fixture import BeaconsClientV1Fixture


class TestBeaconsMockClientV1:
    @classmethod
    def setup_class(cls):
        cls.client = BeaconsMockClientV1()
        cls.fixture = BeaconsClientV1Fixture(cls.client)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_calculate_position(self):
        self.fixture.test_calculate_position()