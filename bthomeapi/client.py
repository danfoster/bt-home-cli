import hashlib
import logging
import requests
import json
from pprint import pprint

logger = logging.getLogger(__name__)

class ApiClient:
    """
    API Client class for BT Home Wifi

    arguments:
        ipaddr: The IP address of a Disc
        username: The username, usually "admin"
        password: The "Admin Password" as found on the disc
    """
    def __init__(self, ipaddr, username, password):
        self.request_endpoint = "/cgi/json-req"
        self.session = requests.Session()
        
        # These get updated after the first login
        self.session_id = 0
        # self.nonce = 2818586228
        self.nonce = 3375479880

        self.id_counter = 0
        self.username = username
        self.password = password
        self.ipaddr = ipaddr

    @staticmethod
    def hash(inputstring):
        """
        Hashes the input, currently only supports MD5 hashes. But the offical JS client
        appears to potentially support SHA1.
        """
        #TODO: support GUI_ACTIVATE_SHA512ENCODE_OPT
        return hashlib.md5(inputstring.encode()).hexdigest()

    def digest_auth(self, nonce):
        """
        Generates a hash suitable for using with digest auth.

        Returns the auth hash
        """
        lnonce=""

        passhash=self.hash(self.password)
        logger.debug("passhash is: %s", passhash)
        ha1 = self.hash("{}:{}:{}".format(self.username, lnonce, passhash))
        logger.debug("ha1 is %s", ha1)
        authkey = self.hash("{}:{}:{}:{}:{}".format(ha1, self.id_counter, nonce, "JSON", self.request_endpoint))
        logger.debug("authkey is: %s", authkey)

        return authkey

    def action(self, actions, priority=False):
        """
        Performs a pre-formatted action

        parameters:
            actions: A object representing a list of actions.
        """
        auth_key = self.digest_auth(self.nonce)
        data = {
            "request": {
                "actions": actions,
                "auth-key": auth_key,
                "cnonce": self.nonce,
                "id": self.id_counter,
                "priority": priority,
                "session-id": self.session_id,
            }
        }
        logger.debug("Payload: %s", data)
        r = self.session.post("http://{}{}".format(self.ipaddr, self.request_endpoint), data = {'req': json.dumps(data)})
        r.raise_for_status()
        self.id_counter += 1
        return r.json()

    def login(self):
        """
        Performs to login dance, setting self.session_id and self.nonce
        """
        actions = [
            {
                'id': 0,
                'method': 'logIn',
                'parameters': {
                    'persistent': 'true',
                    'session-options': {
                        'capability-depth': 2,
                        'capability-flags': {
                            'default-value': False,
                            'description': False,
                            'name': True,
                            'restriction': True
                        },
                        'context-flags': {
                            'get-content-name': True,
                            'local-time': True
                        },
                        'language': 'ident',
                        'nss': [
                            {
                                'name': 'gtw',
                                'uri': 'http://sagemcom.com/gateway-data'
                            }
                        ],
                        'time-format': 'ISO_8601'
                    },
                    'user': self.username
                }
            }
        ]
        result = self.action(actions)
        logger.debug("Result: %s", result)
        params = result['reply']['actions'][0]['callbacks'][0]['parameters']
        self.session_id = params['id']
        self.nonce = params['nonce']
