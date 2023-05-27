#!/usr/bin/env python3

import asyncio
from mavsdk import System

async def goto(drone, x, y, absolute_alt, target_alt):
    flying_alt = absolute_alt + target_alt
    await drone.action.goto_location(47.3977408 + (y/(111139)), 8.545592899999999 + (x/(111139)), flying_alt, 0)

async def run():
    drone = System()
    await drone.connect(system_address="udp://:14540")

    print("Waiting for drone to connect...")
    async for state in drone.core.connection_state():
        if state.is_connected:
            print(f"-- Connected to drone!")
            break

    print("Waiting for drone to have a global position estimate...")
    async for health in drone.telemetry.health():
        if health.is_global_position_ok and health.is_home_position_ok:
            print("-- Global position state is good enough for flying.")
            break

    print("Fetching amsl altitude at home location....")
    async for terrain_info in drone.telemetry.home():
        absolute_altitude = terrain_info.absolute_altitude_m
        break

    print("-- Arming")
    await drone.action.arm()

    print("-- Taking off")
    await drone.action.takeoff()

    await asyncio.sleep(5)
    # To fly drone 20m above the ground plane

    # goto_location() takes Absolute MSL altitude

    await goto(drone, 0, 0, absolute_altitude, 20)

    await asyncio.sleep(10)

    await goto(drone, 15, 30, absolute_altitude, 20)
    await asyncio.sleep(10)

    await goto(drone, 0, 30, absolute_altitude, 20)

    #Put this code in if you want to output the drone's position
    #async for position in drone.telemetry.position():
    #    print(position)


if __name__ == "__main__":
    # Run the asyncio loop
    asyncio.run(run())
