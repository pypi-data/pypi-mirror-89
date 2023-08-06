from typing import List

from .bluvo_interface import BLUvoInternalInterface, BLUvoConfig, VehicleInterface
from .helpers.either import Either


class BLUvoEu(BLUvoInternalInterface):

    def __init__(self, bluvo_config: BLUvoConfig):
        super().__init__(bluvo_config)

    def login(self):
        pass

    def verify_pin(self, pin: str):
        pass

    def get_vehicles(self) -> List[VehicleInterface]:
        pass

    def request(self, cmd, data=None, headers=None) -> Either[dict, str]:
        pass