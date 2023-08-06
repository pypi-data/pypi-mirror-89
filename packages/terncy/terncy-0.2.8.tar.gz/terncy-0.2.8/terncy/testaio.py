#!/usr/bin/env python
# -*- coding: utf-8 -*-

import aiohttp
import asyncio
import ssl
import terncy
from datetime import datetime


async def foo():
    return "bar"

def event_hander(t, msg):
    print("now: ", datetime.now())
    print("got event", msg)

async def main():
    t = terncy.Terncy(
        "homeass_nbhQ43",
        "192.168.2.187",
        443,
        "homeassistant_user",
        "0269c4ce3f0440a3ab409433ba7440fc",
    )
    t = terncy.Terncy(
        "homeass_nbhQ43",
        "192.168.1.109",
        443,
        "b01f3fc64d1b372db6e7cfa6285a8762",
        "a8221b80-10d8-11eb-e2bf-4320fdb61f78",
    )
    t.register_event_handler(event_hander)
    # await t.check_token_state(3, "0269c4ce3f0440a3ab409433ba7440fc")
    # await t.start()
    asyncio.ensure_future(t.start())
    print("after ws started")
    # await t.discover()
    await asyncio.sleep(5)


loop = asyncio.get_event_loop()
loop.run_until_complete(main())

