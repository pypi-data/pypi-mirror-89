# -*- coding: utf-8 -*-
"""
    step8.test.TestBeaconMemoryPersistence
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TestBeaconMemoryPersistence class

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
from pip_beacons_sample_python.persistence.BeaconsMemoryPersistence import BeaconsMemoryPersistence
from .BeaconsPersistenceFixture import BeaconsPersistenceFixture


class TestBeaconMemoryPersistence():
    @classmethod
    def setup_class(cls):
        cls.persistence = BeaconsMemoryPersistence()
        cls.fixture = BeaconsPersistenceFixture(cls.persistence)

    def setup_method(self, method):
        self.persistence.clear(None)

    def test_crud_operations(self):
        self.fixture.test_crud_operations()

    def test_get_with_filter(self):
        self.fixture.test_get_with_filter()

