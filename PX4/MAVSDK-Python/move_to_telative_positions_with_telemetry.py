#!/usr/bin/env python3

import asyncio
from mavsdk import System
from mavsdk import (OffboardError, PositionNedYaw)


async def run():
    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Set parameters
    await drone.param.set_float_param("MIS_TAKEOFF_ALT", 1.0)  # set takeoff height to 1 meter
    await drone.param.set_int_param("COM_TAKEOFF_ACT", 0)  # hold after takeoff
    await drone.param.set_int_param("COM_OBL_ACT", 0)  # 0: land if lost offboard signal; 1: hold if lost offboard signal

    # Start parallel tasks
    asyncio.ensure_future(print_altitude(drone))
    asyncio.ensure_future(print_flight_mode(drone))
    termination_task = asyncio.ensure_future(observe_is_in_air(drone))

    # Execute the maneuvers
    print("-- Arming")
    try:
        await drone.action.arm()
    except Exception as e:
        print(e)

    #print("-- Taking off")
    # await drone.action.takeoff()

    # await asyncio.sleep(10)  # stay in there for 10 seconds

    print("-- Setting initial setpoint")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, 0.0, 0.0))

    print("-- Starting offboard")
    try:
        await drone.offboard.start()
    except OffboardError as error:
        print(f"Starting offboard mode failed with error code: {error._result.result}")
        print("-- Disarming")
        await drone.action.disarm()
        return

    await asyncio.sleep(1)

    print("-- Go up 0.5 m")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(1)

    print("-- Go 1m North, 0m East, -0.5m Down (actually 0.5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(1.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(1)

    print("-- Back to start point: Go 0m North, 0m East, -0.5m Down (actually 0.5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(1)

    print("-- Go -1m North, 0m East, -0.5m Down (actually 0.5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(-1.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(1)

    print("-- Back to start point: Go 0m North, 0m East, -0.5m Down (actually 0.5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -0.5, 0.0))
    await asyncio.sleep(1)

    print("-- Stopping offboard")
    try:
        await drone.offboard.stop()
    except OffboardError as error:
        print(f"Stopping offboard mode failed with error code: {error._result.result}")

    print("-- Landing")
    await drone.action.land()

    # Wait until the drone is landed (instead of returning after 'land' is sent)
    await termination_task


async def print_altitude(drone):
    """ Prints the altitude when it changes """

    previous_altitude = None

    async for position in drone.telemetry.position():
        altitude = round(position.relative_altitude_m)
        if altitude != previous_altitude:
            previous_altitude = altitude
            print(f"Altitude: {altitude}")


async def print_flight_mode(drone):
    """ Prints the flight mode when it changes """

    previous_flight_mode = None

    async for flight_mode in drone.telemetry.flight_mode():
        if flight_mode is not previous_flight_mode:
            previous_flight_mode = flight_mode
            print(f"Flight mode: {flight_mode}")


async def observe_is_in_air(drone):
    """ Monitors whether the drone is flying or not and
    returns after landing """

    was_in_air = False

    async for is_in_air in drone.telemetry.in_air():
        if not is_in_air:
            print("Not in the air now.")
            # await drone.action.kill()
            await drone.action.disarm()
            await asyncio.get_event_loop().shutdown_asyncgens()
            return

        #if is_in_air:
        #    was_in_air = is_in_air

        #if was_in_air and not is_in_air:
        #    print("Not in the air now.")
        #    # await drone.action.kill()
        #    await drone.action.disarm()
        #    await asyncio.get_event_loop().shutdown_asyncgens()
        #    return


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
