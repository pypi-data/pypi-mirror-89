# -*- coding: utf-8 -*-
"""
    step8.test.TestBeaconsHttpServiceV1
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    TestBeaconsHttpServiceV1 class

    :copyright: Conceptual Vision Consulting LLC 2018-2019, see AUTHORS for more details.
    :license: MIT, see LICENSE for more details.
"""
import json
import time

import requests
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.errors import InvocationException
from pip_services3_commons.refer import References, Descriptor
from pip_services3_commons.run import Parameters

from pip_beacons_sample_python.data.version1 import BeaconV1, BeaconTypeV1
from pip_beacons_sample_python.logic.BeaconsController import BeaconsController
from pip_beacons_sample_python.persistence.BeaconsMemoryPersistence import BeaconsMemoryPersistence
from pip_beacons_sample_python.services.version1.BeaconsHttpServiceV1 import BeaconsHttpServiceV1

BEACON1 = BeaconV1("1", "1", BeaconTypeV1.AltBeacon, "00001", "TestBeacon1", {"type": 'Point', "coordinates": [0, 0]}, 50.0)
BEACON2 = BeaconV1("2", "1", BeaconTypeV1.iBeacon, "00002", "TestBeacon2", {"type": 'Point', "coordinates": [2, 2]}, 70.0)
BEACON3 = BeaconV1("3", "2", BeaconTypeV1.AltBeacon, "00003", "TestBeacon3", {"type": 'Point', "coordinates": [10, 10]}, 50.0)

class TestBeaconsHttpServiceV1():
    @classmethod
    def setup_class(cls):
        cls._persistence = BeaconsMemoryPersistence()
        cls._controller = BeaconsController()
        cls._service = BeaconsHttpServiceV1()

        cls._service.configure(ConfigParams.from_tuples(
            'connection.protocol', 'http',
            'connection.port', 3002,
            'connection.host', 'localhost'))

        references = References.from_tuples(Descriptor('beacons', 'persistence', 'memory', 'default', '1.0'),
                                            cls._persistence,
                                            Descriptor('beacons', 'controller', 'default', 'default', '1.0'),
                                            cls._controller,
                                            Descriptor('beacons', 'service', 'http', 'default', '1.0'),
                                            cls._service)
        cls._controller.set_references(references)
        cls._service.set_references(references)

        cls._persistence.open(None)
        cls._service.open(None)

    @classmethod
    def teardown_class(cls):
        cls._persistence.close(None)
        cls._service.close(None)

    def test_crud_operations(self):
        time.sleep(2)
        # Create the first beacon
        beacon1 = self.invoke("/v1/beacons/create_beacon", Parameters.from_tuples("beacon", BEACON1))

        assert beacon1 != None
        assert beacon1['id'] == BEACON1['id']
        assert beacon1['site_id'] == BEACON1['site_id']
        assert beacon1['udi'] == BEACON1['udi']
        assert beacon1['type'] == BEACON1['type']
        assert beacon1['label'] == BEACON1['label']
        assert beacon1['center'] != None

        # Create the second beacon
        beacon2 = self.invoke("/v1/beacons/create_beacon", Parameters.from_tuples("beacon", BEACON2))

        assert beacon2 != None
        assert beacon2['id'] == BEACON2['id']
        assert beacon2['site_id'] == BEACON2['site_id']
        assert beacon2['udi'] == BEACON2['udi']
        assert beacon2['type'] == BEACON2['type']
        assert beacon2['label'] == BEACON2['label']
        assert beacon2['center'] != None

        # Get all beacons
        page = self.invoke("/v1/beacons/get_beacons", Parameters.from_tuples("beacons"))
        assert page != None
        assert len(page['data']) == 2

        beacon1 = page['data'][0]

        # Update the beacon
        beacon1['label'] = "ABC"
        beacon = self.invoke("/v1/beacons/update_beacon", Parameters.from_tuples("beacon", beacon1))
        assert beacon != None
        assert beacon1['id'] == beacon['id']
        assert "ABC" == beacon['label']

        # Get beacon by udi
        beacon = self.invoke("/v1/beacons/get_beacon_by_udi", Parameters.from_tuples("udi", beacon1['udi']))
        assert beacon != None
        assert beacon['id'] == beacon1['id']

        # Calculate position for one beacon
        position = self.invoke("/v1/beacons/calculate_position", Parameters.from_tuples("site_id", '1', "udis", ['00001']))
        assert position != None
        assert "Point" == position["type"]
        assert 2 == len(position["coordinates"])
        assert 0 == position["coordinates"][0]
        assert 0 == position["coordinates"][1]

        # Delete beacon
        self.invoke("/v1/beacons/delete_beacon_by_id", Parameters.from_tuples("id", beacon1['id']))

        # Try to get deleted beacon
        beacon = self.invoke("/v1/beacons/get_beacon_by_id", Parameters.from_tuples("id", beacon1['id']))
        assert beacon == False

    def invoke(self, route, entity):
        params = {}
        route = "http://localhost:3002" + route
        response = None
        timeout = 10000
        try:
            # Call the service
            data = json.dumps(entity)
            response = requests.request('POST', route, params=params, json=data, timeout=timeout)
            return response.json()
        except Exception as ex:
            return False