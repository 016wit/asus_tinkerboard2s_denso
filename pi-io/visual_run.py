import asyncio
import datetime
import json
import os
from aiohttp import web
from functools import partial

from cloud_108 import Cloud108
from engin_core import StateControl
from engin_core import loggin
from engin_core import ConfigLoader
from web_service.web_app import web_loop

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_ACTUAL = os.path.dirname(os.path.abspath(__file__))
connected = set()
queue = asyncio.Queue()
config = {}
state = {
    "actual": 0,
    "pp_plan": 1222,
    "att": 10.2,
    "loss_time": "00:02:30",
    "tt": 10.3,
    "last_time": datetime.datetime.now(),
}
version = "1.1.10"
platform = Cloud108(serial="AK204110107000099")

async def data_accquired():
    start = 0
    print('Start Data acc')
    last = datetime.datetime.now()
    while True:
        start += 1
        current = datetime.datetime.now()
        diff = current - last
        print('Current {} ---> Diff {}'.format(current, diff))
        await asyncio.sleep(1)


async def ws_handler(websocket, path):
    # register(websocket) sends user_event() to websocket
    print(path)
    connected.add(websocket)
    try:
        # Implement logic here.
        async for message in websocket:
            print(message)
        await asyncio.sleep(1)
    except Exception as e:
        print(e)
    finally:
        # Unregister.
        print('unregister')
        connected.remove(websocket)


async def on_web_start(app, *args, **kwargs):
    asyncio.create_task(data_accquired())


if __name__ == '__main__':
    config_loader = ConfigLoader(host='homecloud.p-enterprise.com:8080', path=BASE_DIR)
    config_loader.load_config()
    # config_loader.dump_config()
    sc1 = StateControl(config_loader=config_loader, config=config_loader.config, logs=loggin.log_text, path=BASE_DIR,
                       version=version, load_state_file="state1", load_config_file="config1")
    # sc2 = StateControl(config_loader=config_loader, config=config_loader.config, logs=loggin.log_text, path=BASE_DIR,
    #                    version=version, load_state_file="state2", load_config_file="config2")

    sc_pool = [sc1, ]

    # for x in sc_pool:
    #     x.load_state(BASE_DIR)
    #     x.config_loader.load_meta()
    #     x.config = x.config_loader.config
    #     x.cal_target()
    # print(sc.is_idle)
    platform.init_mqtt()
    # asyncio.get_event_loop().create_task(web_loop(sc))
    # asyncio.get_event_loop().run_forever()
    # with open('./state.json', 'w') as outfile:
    #     dump_state = { **state }
    #     dump_state['last_time'] = dump_state['last_time'].strftime('%Y-%m-%d %H:%M:%S.%f')
    #     json.dump(dump_state, outfile)
    # asyncio.get_event_loop().create_task(data_accquired())
    # asyncio.get_event_loop().run_until_complete(start_server)
    # asyncio.get_event_loop().run_forever()
    try:
        asyncio.get_event_loop().create_task(data_accquired())
        # asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_forever()
        web_loop(sc_pool, None, None)
    finally:
        for x in sc_pool:
            x.dump_state(BASE_DIR)

    print("Exit process")
