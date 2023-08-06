# -*- coding: utf-8 -*-
import copy
from typing import List

from pip_services3_commons.data import FilterParams, IdGenerator, PagingParams, DataPage

from pip_beacons_sample_python.clients.version1.IBeaconsClientV1 import IBeaconsClientV1
from pip_beacons_sample_python.data.version1 import BeaconV1

filtered = filter


class BeaconsMockClientV1(IBeaconsClientV1):
    _max_page_size = 100
    _items: List[BeaconV1] = []

    def compose_filter(self, filter):
        filter = filter or FilterParams()
        id = filter.get_as_nullable_string("id")
        site_id = filter.get_as_nullable_string("site_id")
        label = filter.get_as_nullable_string('label')
        udi = filter.get_as_nullable_string('udi')
        udis = filter.get_as_object('udis')

        if type(udis) == str:
            udis = udis.split(',')

        if not (type(udis) == list):
            udis = None

        def filter_beacons(item):
            if id is not None and item.id != id:
                return False
            if site_id is not None and item.site_id != site_id:
                return False
            if label is not None and item.label != label:
                return False
            if udi is not None and item.udi != udi:
                return False
            if udis is not None:
                try:
                    udis.index(item.udi)
                except Exception as e:
                    return False
            return True

        return filter_beacons

    def get_beacons(self, correlation_id, filter, paging):
        filter_beacons = self.compose_filter(filter)
        beacons = [item for item in self._items if filter_beacons(item) is True]

        # Extract a page
        paging = paging if paging is not None else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)
        total = None
        if paging.total:
            total = len(beacons)
        if skip > 0:
            beacons = beacons[skip:]
            beacons = beacons[:take]

        page = DataPage(beacons, total)
        return page

    def get_beacon_by_id(self, correlation_id, id):
        beacons = [item for item in self._items if item.id == id]
        beacon = beacons[0] if len(beacons) > 0 else None
        return beacon

    def get_beacon_by_udi(self, correlation_id, udi):
        beacons = [item for item in self._items if item.udi == udi]
        beacon = beacons[0] if len(beacons) > 0 else None
        return beacon

    def get_beacons_by_filter(self, correlation_id, filter, paging, sort=None, select=None):
        items = list(self._items)

        # Filter and sort
        if not (filter is None):
            items = list(filtered(filter, items))
        if not (sort is None):
            items = list(items.sort(key=sort))
            # items = sorted(items, sort)

        # Prepare paging parameters
        paging = paging if not (paging is None) else PagingParams()
        skip = paging.get_skip(-1)
        take = paging.get_take(self._max_page_size)

        # Get a page
        data = items
        if skip > 0:
            data = data[skip:]
        if take > 0:
            data = data[:take + 1]

        # Convert values
        if not (select is None):
            data = map(select, data)

        # Return a page
        return DataPage(data, len(items))

    def calculate_position(self, correlation_id, site_id, udis):
        beacons: List[BeaconV1]
        position = None

        if udis is None or len(udis) == 0:
            return

        page = self.get_beacons(correlation_id, FilterParams.from_tuples(
            'site_id', site_id,
            'udis', udis
        ), None)
        beacons = page.data if page.data else []

        lat = 0
        lng = 0
        count = 0

        for beacon in beacons:
            if beacon['center'] != None and beacon['center']['type'] == "Point" and len(
                    beacon['center']['coordinates']) > 1:
                lng = lng + beacon['center']['coordinates'][0]
                lat = lat + beacon['center']['coordinates'][1]
                count = count + 1

        if count > 0:
            position = {"type": 'Point', "coordinates": [lng / count, lat / count]}
            return position
        return None

    def create_beacon(self, correlation_id, beacon):
        if beacon is None:
            return

        beacon = copy.deepcopy(beacon)
        beacon.id = beacon.id or IdGenerator.next_long()
        self._items.append(beacon)
        return beacon

    def update_beacon(self, correlation_id, beacon):
        try:
            index = list(map(lambda x: x.id, self._items)).index(beacon.id)
        except ValueError:
            return

        beacon = copy.deepcopy(beacon)
        self._items[index] = beacon
        return beacon

    def delete_beacon_by_id(self, correlation_id, beacon_id):
        try:
            index = list(map(lambda x: x.id, self._items)).index(beacon_id)
        except ValueError:
            return
        del self._items[index]
        return beacon_id
