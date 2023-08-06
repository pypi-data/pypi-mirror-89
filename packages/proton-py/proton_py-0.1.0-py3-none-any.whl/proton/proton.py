import requests
import logging

from .connection import Connection

DEFAULT_TIMEOUT = 5  # seconds
logging.basicConfig(format='%(asctime)s - %(levelname)s : %(message)s', level=logging.INFO, datefmt='%m/%d/%Y %I:%M:%S %p')

class Proton:
    connection_constructor = Connection

    def __init__(self, token=None):
        # self.timeout = DEFAULT_TIMEOUT
        self.base_url = 'https://api.proton-graph.cloud'
        
        if token is None:
            raise ValueError("Token must be provided.")
        else:
            self.headers = {
                'Ocp-Apim-Subscription-Key': token
            }

        self.con = self.connection_constructor(headers=self.headers)

    def location(self, **kwargs):
        from .location import Location
        return Location(parent=self)