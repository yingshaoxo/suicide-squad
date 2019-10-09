#!/usr/bin/env python3

import asyncio
from mavsdk import System


async def run():
    """
    This is the "main" function.
    It first creates the drone object and initializes it.

    Then it registers tasks to be run in parallel (one can think of them as threads):
        - print_altitude: print the altitude
        - print_flight_mode: print the flight mode
        - observe_is_in_air: this monitors the flight mode and returns when the
                             drone has been in air and is back on the ground.

    Finally, it goes to the actual works: arm the drone, initiate a takeoff
    and finally land.

    Note that "observe_is_in_air" is not necessary, but it ensures that the
    script waits until the drone is actually landed, so that we receive feedback
    during the landing as well.
    """

    # Init the drone
    drone = System()
    await drone.connect(system_address="udp://:14540")

    # Set parameters
    await drone.param.set_float_param("MIS_TAKEOFF_ALT", 1.0)  # set takeoff height to 1 meter
    await drone.param.set_int_param("COM_TAKEOFF_ACT", 1)  # hold after takeoff

    # Start parallel tasks
    asyncio.ensure_future(print_altitude(drone))
    asyncio.ensure_future(print_flight_mode(drone))
    termination_task = asyncio.ensure_future(observe_is_in_air(drone))

    # Execute the maneuvers
    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(10)  # stay in there for 10 seconds

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
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            return


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())