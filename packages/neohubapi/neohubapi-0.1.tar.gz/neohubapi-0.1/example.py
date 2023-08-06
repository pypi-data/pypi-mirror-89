#!/usr/bin/env python3

# SPDX-FileCopyrightText: 2020 Andrius Štikonas <andrius@stikonas.eu>
# SPDX-License-Identifier: MIT


import asyncio
import datetime
import logging
import neohubapi.neohub as neohub

from neohubapi.enums import ScheduleFormat


async def run():
    hub = neohub.NeoHub()
    await hub.connect()
    system = await hub.get_system()
    hub_data, thermostats = await hub.get_live_data()
    for device in thermostats:
        print(f"Rate of change of {device.name}: {await device.rate_of_change}")
        await device.identify()

    print(await hub.target_temperature_step)


logging.basicConfig(level=logging.DEBUG)
asyncio.run(run())
