import logging

log = logging.getLogger(__name__)

API_VERSION = 'v2'

class Location:
    _endpoints = {
        'get_all_locations': '/{api_version}/locations/dump',
        'get_location': '/{api_version}/locations/{id}',
        'get_location_feature': '/{api_version}/locationfeatures/{id}'
    }

    def __init__(self, parent=None):
        if parent is None:
            raise ValueError('Class must have a parent object.')
        self.con = parent.con
        self.location_url = parent.base_url + '/public/locations/api'

    def get_all_locations(self):
        """Provides the listing of all Locations available with their names and numbers only.
        This is good for caching purposes."""

        path = self.location_url + self._endpoints.get('get_all_locations').format(api_version=API_VERSION)
        response = self.con.get(path)

        if not response:
            return None
        data = response.json()
        return data

    def get_location_by_id(self, id, **params):
        path = self.location_url + self._endpoints.get('get_location').format(api_version=API_VERSION, id=id) 
        response = self.con.get(path, params=params if params else None)

        if not response:
            return None
        data = response.json()
        return data

    def get_location_feature_by_id(self, id):
        path = self.location_url + self._endpoints.get('get_location_feature').format(api_version=API_VERSION, id=id) 
        response = self.con.get(path)

        if not response:
            return None
        data = response.json()
        return data

