import requests
import json
import logging

from datetime import datetime

from .bluvo_interface import BLUvoInternalInterface, BLUvoSession
from .helpers.either import Either
from .vehicles.ca_vehicle import BLUvoCaVehicle


class BLUvoCa(BLUvoInternalInterface):

    def __init__(self, bluvo_config):
        super().__init__(bluvo_config)
        self.bluvo_config = bluvo_config
        self.session = BLUvoSession(None, None, 0)

    def request(self, cmd, data=None, headers=None) -> Either[dict, str]:

        if headers is None:
            headers = {}

        if data is None:
            data = {}

        default_headers = {
            'content-type': 'application/json;charset=UTF-8',
            'accept': 'application/json, text/plain, */*',
            'accept-encoding': 'gzip, deflate, br',
            "from": 'SPA',
            "language": "1",
            "offset": "-5",
            "accessToken": self.session.access_token
        }

        default_data = {
            'pin': self.bluvo_config.pin
        }

        req = requests.post(self.bluvo_config.base_url + cmd,
                            headers={**default_headers, **headers},
                            data=json.dumps({**default_data, **data}))

        print("{}: {}".format(cmd, req.status_code))

        if req.status_code != requests.codes.ok:
            logging.error('%s: %s' % ("HttpError", req.status_code))
            return Either[dict, str].right("HttpError")

        response = req.json()

        if "error" in response:
            logging.error('%s: %s' % ("InvalidRequest", response["error"]))
            return Either[dict, str].right("InvalidRequest")

        print(req.json())
        return Either[dict, str].left(req.json())

    def handle_session_login(self, res):
        self.session = BLUvoSession(
            res['result']['accessToken'],
            res['result']['refreshToken'],
            res['result']['expireIn'])

    def handle_exception(self, err):
        print(err)
        pass

    def login(self):

        response = self.request("lgn", data={
            'loginId': self.bluvo_config.username,
            'password': self.bluvo_config.password
        })

        response.match(self.handle_session_login, self.handle_exception)

    def refresh_token(self):
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        should_refresh = timestamp - self.session.token_expires_at <= 10

        if self.session.refresh_token and should_refresh:
            response = self.request("vrfytnc")

            response.match(self.handle_session_login, self.handle_exception)

    def verify_pin(self):
        response = self.request("vrfypin")

        pin_token = response.match(
            lambda res: res['result']['pAuth'],
            self.handle_exception)

        self.session.set_pin_token(pin_token)

    def get_vehicles(self):
        response = self.request("vhcllst")
        # self.verify_pin()
        # location_response = self.request("fndmcr", {'pAuth': self.session.pin_token})

        return response.match(
            lambda res: [
                BLUvoCaVehicle(self, self.bluvo_config, vehicle_info)
                for vehicle_info in res['result']['vehicles']],
            self.handle_exception)