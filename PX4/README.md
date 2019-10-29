# How to use PX4

## Some words
* HITL: hardware in the loop
* SITL: software in the loop
* CBRK: circuit breaker
* altitude mode: In this mode, the drone will keep a certain height, but drafts horizontally.
* position mode: At this mode, the drone will keep stay at a point, no drafts, just still in there.

## Paramaters
* EKF2_AID_MASK: set to `use optical flow` only

* CBRK_SUPPLY_CHK: set to `no check`
* CBRK_USB_CHK: set to `no check`

* MAV_0_CONFIG: set to `TELEM 1` if you plug raspebrry_pi with that port
* MAV_0_MODE: set to `Onboard`
* MAV_0_RATE: set to `1200 B/s`
* SER_TEL1_BAUD: set to `57600 8N1` if you use `TELEM 1` port

* COM_OBL_ACT: set to `land` if lost of offboard signal
* COM_OBL_RC_ACT: set to `land` if lost of RC signal too

* CBRK_IO_SAFETY: set to `no check`, so you don't have to click safety button before you arm

## We use `jMAVSIM` and `MAVSDK-Python` for software development

### Install
* https://github.com/mavlink/MAVSDK-Python
* https://dev.px4.io/v1.9.0/en/setup/dev_env_linux.html

### Document for development
* https://mavsdk.mavlink.io/develop/en/api_reference/
* https://docs.px4.io/v1.9.0/en/advanced_config/parameter_reference.html
* https://github.com/mavlink/MAVSDK-Python/issues

### The codes may look like
```python
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
    #await drone.action.takeoff()

    #await asyncio.sleep(10)  # stay in there for 10 seconds

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

    await asyncio.sleep(5)

    print("-- Go up 5 m")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)

    print("-- Go 5m North, 0m East, -5m Down (actually 5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(5.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)

    print("-- Back to start point: Go 0m North, 0m East, -5m Down (actually 5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)

    print("-- Go -5m North, 0m East, -5m Down (actually 5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(-5.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)

    print("-- Back to start point: Go 0m North, 0m East, -5m Down (actually 5m high from ground) within local coordinate system, turn to face East")
    await drone.offboard.set_position_ned(PositionNedYaw(0.0, 0.0, -5.0, 0.0))
    await asyncio.sleep(5)

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
        if is_in_air:
            was_in_air = is_in_air

        if was_in_air and not is_in_air:
            await asyncio.get_event_loop().shutdown_asyncgens()
            print("Not in the air now.")
            return


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(run())
```

## MAVProxy
### If you want to use Raspberry_Pi to control your `jMAVSIM` simulator
1. we assume the raspberry_pi ip address is `192.168.43.7`
2. In the compurter that you run a simulator, run this command: 
```
mavproxy.py --master=udp:127.0.0.1:14540 --master=udp:127.0.0.1:14550 --master=udp:127.0.0.1:14560 --out=udp:192.168.43.7:14540 --out=udp:192.168.43.7:14550 --out=udp:192.168.43.7:14560
```
> (out=udp:the_ip_of_computer_where_you_run_your_mavsdk_python_script)
3. In the raspberry_pi, you run the code with:
```
await drone.connect(system_address="udp://:14540")
```

### If you want to use Raspberry_Pi to control the real drone (hardware)
In your raspberry_pi, run the following:
```
mavproxy.py --master=/dev/ttyUSB0 --out=udp:127.0.0.1:14540 --out=udp:127.0.0.1:14550 --out=udp:127.0.0.1:14560 --out=udp:192.168.43.31:14540 --out=udp:192.168.43.31:14550 --out=udp:192.168.43.31:14560 --daemon
```
> /dev/ttyUSB0 has to be right connected. You can reference this: https://dev.px4.io/master/en/companion_computer/pixhawk_companion.html#hardware-setup

You have to click the safety_buttom first, then use remote controller to arm, then you are able to run the Python codes to control the drone

## Battery
### For charging
```
Lipo 
2.0A 11.1V(3S)
```

### For configure
```
Number of Cells: 3
Full Voltage: 4.2
Empty Voltage: 3.6
```