from . import test_config as cfg

from .api.bluvo_interface import VehicleStatus, VehicleLocation, BLUvoConfig
from .api.helpers.constants import Regions, Makes
from . import BLUvo


def print_status(status: VehicleStatus):
    print (status.chassis.locked)
    print (status.climate.temperature_set_point)
    pass


def print_location(location: VehicleLocation):
    print("{}, {}".format(location.latitude, location.longitude))


def handle_exception(ex):
    print(ex)


if __name__ == "__main__":
    config = BLUvoConfig(Regions.CA, Makes.KIA, cfg.username, cfg.password, cfg.pin)
    ctrl = BLUvo(config)

    ctrl.login()
    vehicles = ctrl.get_vehicles()

    first_vehicle = vehicles[0]

    first_vehicle.location().match(print_location, handle_exception)
    first_vehicle.status().match(print_status, handle_exception)
