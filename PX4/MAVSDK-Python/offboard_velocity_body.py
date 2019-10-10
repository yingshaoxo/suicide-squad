#!/usr/bin/env python3

"""
Some caveats when attempting to run the examples in non-gps environments:

- `drone.action.arm()` will return a `COMMAND_DENIED` result because the action requires switching
  to LOITER mode first, something that is currently not supported in a non-gps environment. You will
  need to temporarily disable this part here:
  `https://github.com/mavlink/MAVSDK/blob/develop/plugins/action/action_impl.cpp#L61-L65`

- `drone.offboard.stop()` will also return a `COMMAND_DENIED` result because it requires a mode
  switch to HOLD, something that is currently not supported in a non-gps environment.
"""

import asyncio

from mavsdk import System
from mavsdk import (OffboardError, VelocityBodyYawspeed)


async def run():
    """ Does Offboard control using velocity body coordinates. """

    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Set parameters
    await drone.param.set_float_param("MIS_TAKEOFF_ALT", 1.0)  # set takeoff height to 1 meter
    await drone.param.set_int_param("COM_TAKEOFF_ACT", 0)  # hold after takeoff
    await drone.param.set_int_param("COM_OBL_ACT", 0)  # 0: land if lost offboard signal; 1: hold if lost offboard signal

    # Start parallel tasks
    asyncio.ensure_future(print_altitude(drone))

    print("-- Arming")
    await drone.action.arm()

    print("-- Setting initial setpoint")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    print("-- Turn clock-wise and climb")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, -1, 0.0))
    await asyncio.sleep(5)

    print("-- Turn clock-wise and climb")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.1, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, -0.1, 0.0, 0.0))
    await asyncio.sleep(5)

    print("-- Wait for a bit")
    await drone.offboard.set_velocity_body(VelocityBodyYawspeed(0.0, 0.0, 0.0, 2.0))
    await asyncio.sleep(20)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Landing")
    await drone.action.land()


async def print_altitude(drone):
    """ Prints the altitude when it changes """

    previous_altitude = None

    async for position in drone.telemetry.position():
        altitude = round(position.relative_altitude_m)
        if altitude != previous_altitude:
            previous_altitude = altitude
            print(f"Altitude: {altitude}")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
