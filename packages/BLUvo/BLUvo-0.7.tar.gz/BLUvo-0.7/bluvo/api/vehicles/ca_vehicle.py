from ..bluvo_interface import VehicleInterface, BLUvoConfig, VehicleStatus, Chassis, Quadrants, Climate, Engine, \
    VehicleLocation
from ..helpers.dict_helpers import dict_get_path
from ..helpers.either import Either
from ..helpers.temperature_helpers import temp_code_to_celsius


class BLUvoCaVehicle(VehicleInterface):

    def __init__(self, ctrl, bluvo_config: BLUvoConfig, vehicle_info):
        super().__init__(bluvo_config)

        self.ctrl = ctrl
        self.id = vehicle_info["vehicleId"]

    def status(self, refresh=False) -> Either[VehicleStatus, str]:
        response = self.ctrl.request("lstvhclsts" if refresh else "rltmvhclsts", headers={
            "vehicleId": self.id
        })
        print(response)
        return response.match(self.handle_status, lambda ex: Either[VehicleStatus, str].right(ex))

    def handle_status(self, res):
        status = res["result"]["status"]

        return Either[VehicleStatus, str].left(VehicleStatus(
            chassis=Chassis(
                hood_open=status["hoodOpen"],
                trunk_open=status["trunkOpen"],
                locked=status["doorLock"],
                open_doors=Quadrants(
                    front_left=status["doorOpen"]["frontLeft"],
                    front_right=status["doorOpen"]["frontRight"],
                    back_left=status["doorOpen"]["backLeft"],
                    back_right=status["doorOpen"]["backRight"]
                ),
                tire_pressure_warning_lamp=Quadrants(
                    front_left=dict_get_path(status, "tirePressureLamp", "tirePressureWarningLampFrontLeft", default=False),
                    front_right=dict_get_path(status, "tirePressureLamp", "tirePressureWarningLampFrontRight", default=False),
                    back_left=dict_get_path(status, "tirePressureLamp", "tirePressureWarningLampRearLeft", default=False),
                    back_right=dict_get_path(status, "tirePressureLamp", "tirePressureWarningLampRearRight", default=False)
                )
            ),
            climate=Climate(
                active=status["airCtrlOn"],
                steering_wheel_heat=status["steerWheelHeat"] if "steerWheelHeat" in status else False,
                side_mirror_heat=False,
                rear_window_heat=status["sideBackWindowHeat"] if "sideBackWindowHeat" in status else False,
                defrost=status["defrost"],
                temperature_set_point=temp_code_to_celsius(dict_get_path(status, "airTemp", "value", default=None)),
                temperature_unit=dict_get_path(status, "airTemp", "unit", default=0),
            ),
            engine=Engine(
                ignition=status["engine"],
                adaptive_cruise_control=status["acc"],
                range=dict_get_path(status, "dte", "value", default=0),
                charging=dict_get_path(status, "evStatus", "batteryCharge", default=False),
                battery_charge_12v=dict_get_path(status, "battery", "batSoc", default=False),
                battery_charge_hv=dict_get_path(status, "evStatus", "batteryStatus", default=False)
            )
        ))

    def location(self):
        self.ctrl.verify_pin()
        response = self.ctrl.request("fndmcr", headers={
            "vehicleId": self.id
        })
        print(response)
        return response.match(self.handle_location, lambda ex: Either[VehicleStatus, str].right(ex))

    def handle_location(self, res):
        coordinates = res["result"]["coord"]

        return Either[VehicleLocation, str].left(VehicleLocation(
            coordinates["lat"],
            coordinates["lon"],
            coordinates["alt"]
        ))



