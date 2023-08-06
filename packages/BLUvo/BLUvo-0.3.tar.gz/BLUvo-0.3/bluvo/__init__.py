from typing import List

from bluvo.api.bluvo_interface import BLUvoInterface, BLUvoConfig, VehicleInterface
from bluvo.api.ca_hyundai_implementation import BLUvoCaHyundai
from bluvo.api.ca_kia_implementation import BLUvoCaKia
from bluvo.api.helpers.constants import Regions, Makes


class BLUvo(BLUvoInterface):

    impl: BLUvoInterface

    def __init__(self, bluvo_config: BLUvoConfig):
        super().__init__(bluvo_config)

        if bluvo_config.region == Regions.CA and bluvo_config.make == Makes.KIA:
            self.impl = BLUvoCaKia(bluvo_config)
        elif bluvo_config.region == Regions.CA and bluvo_config.make == Makes.HYUNDAI:
            self.impl = BLUvoCaHyundai(bluvo_config)
        # if bluvo_config.region == Regions.US and bluvo_config.make == Makes.KIA:
        #     self.impl = BLUvoUsKia(bluvo_config)
        # if bluvo_config.region == Regions.US and bluvo_config.make == Makes.HYUNDAI:
        #     self.impl = BLUvoUsHyundai(bluvo_config)
        # if bluvo_config.region == Regions.EU and bluvo_config.make == Makes.KIA:
        #     self.impl = BLUvoEuKia(bluvo_config)
        # if bluvo_config.region == Regions.EU and bluvo_config.make == Makes.HYUNDAI:
        #     self.impl = BLUvoEuHyundai(bluvo_config)
        else:
            raise Exception("No Region or Make Implementation")

    def verify_pin(self, pin: str):
        self.impl.verify_pin(pin)

    def login(self):
        self.impl.login()

    def get_vehicles(self) -> List[VehicleInterface]:
        return self.impl.get_vehicles()
