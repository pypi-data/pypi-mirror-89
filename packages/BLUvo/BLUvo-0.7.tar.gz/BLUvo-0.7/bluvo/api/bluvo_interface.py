from abc import abstractmethod
from datetime import datetime
from decimal import Decimal
from typing import List

from .helpers.constants import Regions, Makes
from .helpers.either import Either


class Engine(object):

    def __init__(self,
                 ignition: bool,
                 battery_charge_12v: int,
                 battery_charge_hv: int,
                 charging: bool,
                 range: int,
                 adaptive_cruise_control: bool):
        self.ignition = ignition
        self.battery_charge_12v = battery_charge_12v
        self.battery_charge_hv = battery_charge_hv
        self.charging = charging
        self.range = range
        self.adaptive_cruise_control = adaptive_cruise_control


class Climate(object):
    def __init__(self,
                 active: bool,
                 steering_wheel_heat: bool,
                 side_mirror_heat: bool,
                 rear_window_heat: bool,
                 temperature_set_point: Decimal,
                 temperature_unit: int,
                 defrost: bool):
        self.active = active
        self.steering_wheel_heat = steering_wheel_heat
        self.side_mirror_heat = side_mirror_heat
        self.rear_window_heat = rear_window_heat
        self.temperature_set_point = temperature_set_point
        self.temperature_unit = temperature_unit
        self.defrost = defrost


class Quadrants(object):
    def __init__(self, front_left: bool, front_right: bool, back_left: bool, back_right: bool):
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right


class Chassis(object):
    def __init__(self,
                 hood_open: bool,
                 trunk_open: bool,
                 locked: bool,
                 open_doors: Quadrants,
                 tire_pressure_warning_lamp: Quadrants):
        self.hood_open = hood_open
        self.trunk_open = trunk_open
        self.locked = locked
        self.open_doors = open_doors
        self.tire_pressure_warning_lamp = tire_pressure_warning_lamp


class VehicleStatus(object):
    def __init__(self, engine: Engine, climate: Climate, chassis: Chassis):
        self.engine = engine
        self.climate = climate
        self.chassis = chassis


class VehicleLocation(object):
    def __init__(self, latitude: float, longitude: float, altitude: float):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude


class BLUvoConfig(object):

    def __init__(self, region: Regions, make: Makes, username: str, password: str, pin: str,
                 auto_login=False, vin=None, vehicle_id=None):
        self.vehicle_id = vehicle_id
        self.vin = vin
        self.auto_login = auto_login
        self.pin = pin
        self.password = password
        self.username = username
        self.make = make
        self.region = region

        self.base_url = ""


class BLUvoSession(object):

    def __init__(self, access_token, refresh_token, token_expires_in):
        now = datetime.now()
        timestamp = datetime.timestamp(now)

        self.token_expires_at = timestamp + token_expires_in
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.pin_token = None

    def set_pin_token(self, token):
        self.pin_token = token


class VehicleInterface(object):

    @abstractmethod
    def __init__(self, bluvo_config: BLUvoConfig):
        self.bluvo_config = bluvo_config
        self.id = ""

    def __str__(self):
        return 'Vehicle: %s' % (self.id,)

    def __repr__(self):
        return 'Vehicle: %s' % (self.id,)

    def status(self, refresh=False) -> Either[VehicleStatus, str]:
        return Either[VehicleStatus, str].right("Not Implemented")

    def location(self, refresh=False) -> Either[VehicleLocation, str]:
        return Either[VehicleLocation, str].right("Not Implemented")


class BLUvoInterface(object):

    @abstractmethod
    def __init__(self, bluvo_config: BLUvoConfig):
        pass

    @abstractmethod
    def login(self):
        raise NotImplementedError

    @abstractmethod
    def verify_pin(self, pin: str):
        raise NotImplementedError

    @abstractmethod
    def get_vehicles(self) -> List[VehicleInterface]:
        raise NotImplementedError

    def get_vehicle(self, vehicle_id: str) -> VehicleInterface:
        return next(vehicle for vehicle in self.get_vehicles() if vehicle.id == vehicle_id)


class BLUvoInternalInterface(BLUvoInterface):

    @abstractmethod
    def request(self, cmd, data=None, headers=None) -> Either[dict, str]:
        raise NotImplementedError
