import sys
import asyncio
import os
import datetime
from gpiozero import Button, LED
from functools import partial
from engin_core import StateControl
from engin_core import loggin
from engin_core import ConfigLoader
from cloud_108 import Cloud108
from cloud_108.device import CounterDevice
from web_service.web_app import web_loop

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_ACTUAL = os.path.dirname(os.path.abspath(__file__))
api_host = "localhost"
platform_serial = os.getenv('SERIAL', 'AK204110107000099')
version = "3.0.01"
active_cloud = False
dyn_run = False

if os.getenv('BASE_CONFIG', None):
    BASE_DIR = os.getenv('BASE_CONFIG')

if os.getenv('BASE_ACTUAL', None):
    BASE_ACTUAL = os.getenv('BASE_ACTUAL')

if os.getenv('CLOUD_ACTIVE', False):
    env_cloud_active = os.getenv('CLOUD_ACTIVE', False)
    if env_cloud_active == "TRUE":
        active_cloud = True

if os.getenv('DYN_RUN', False):
    env_dyn_run = os.getenv('DYN_RUN', False)
    if env_dyn_run == "TRUE":
        dyn_run = True

output_1 = LED(17, active_high=False)
output_2 = LED(18, active_high=False)
output_3 = LED(22, active_high=False)
output_4 = LED(27, active_high=False)

input_1 = Button(23)
input_2 = Button(24, bounce_time=0.1)
input_3 = Button(25, bounce_time=0.1)  # Hard reset

output_map = {
    "GPIO23": output_1,
    "GPIO24": output_2,
    "GPIO25": output_3,
}
connected = set()
config = {}
platform = Cloud108(serial=platform_serial, api_host="http://172.16.1.138:5000")
device = [
    CounterDevice("{}-01".format(platform_serial)),
    CounterDevice("{}-02".format(platform_serial))
]

io_tick_time = [
    datetime.datetime.now(),
    datetime.datetime.now()
]


def create_push_frame(state_obj, pt, dev):
    global platform_serial
    df = pt.create_frame()
    idx = 0
    for x in range(len(dev)):
        dev[x].update(state_obj[x])
        dv_f = dev[x].create_frame()
        dv_f[-1] = state_obj[x].service_data
        df = pt.fill_data(df, dv_f, idx, len(dv_f))
        idx += len(dv_f)

    return df


async def logger_tick(state_obj, pt, dev):
    while True:
        try:
            dt = datetime.datetime.now()
            push_frame = create_push_frame(state_obj, pt, dev)
            pt.pushLog(push_frame)
            loggin.push_log(
                "{}/push_log".format(BASE_DIR),
                dt.strftime("%Y_%m_%d"),
                pt.create_push_data(push_frame),
            )

            select_time = dt
            if dt.minute == 0:
                select_time = dt - datetime.timedelta(minutes=1)

            select_idx = "{:02d}:00".format(select_time.hour)
            hour_or = state_obj[0].hour_or[select_idx]
            graph_n = state_obj[0].graph_n[select_idx]
            pt.push_or_result(device[0].serial, {
                "datetime_stamp": select_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "count_val": hour_or["count"],
                "pp_plan_val": int(hour_or["pp_plan"]),
                "or_val": hour_or["or"]
            })
            pt.push_or_analysis(device[0].serial, {
                "datetime_stamp": select_time.strftime("%Y-%m-%dT%H:%M:%S"),
                "lost_val": int(graph_n["lost"]),
                "meeting_val": int(graph_n["meeting"]),
                "run_val": int(graph_n["run"]),
                "down_val": int(graph_n["down"]),
                "short_breakdown_val": int(graph_n["short_breakdown"])
            })

        except Exception as e:
            pt.line_notify(str(e))

        await asyncio.sleep(1 * 60)


async def sys_tick(state_control, pt, dev):
    global platform_serial
    global dyn_run
    topic_read = "{}-01/read".format(platform_serial)
    count = 0
    while True:
        # print('GPIO Service Sys tick', count)
        current_time = datetime.datetime.now()
        for x in state_control:
            if dyn_run:
                if count >= 11 and not x.is_break_time(current_time):
                    x.state_control(current_time, trick=True)
            try:
                x.state_control(current_time, trick=False)
            except Exception as e:
                pass
            x.dump_state(BASE_DIR)

        if active_cloud:
            try:
                df = pt.create_mqtt_push_data(create_push_frame(state_control, pt, dev))
                pt.public_message(topic_read, df)
            except Exception as e:
                print(e)
                pass

        if count >= 11:
            count = 0
        else:
            count += 1

        await asyncio.sleep(1)


def button_press(channel, loop=None, state_control=None):
    # print('Button press :', channel)
    gpio = output_map.get(str(channel.pin))
    if gpio:
        gpio.on()
        current_time = datetime.datetime.now()

        if str(channel.pin) in ["GPIO23", ]:
            diff = current_time - io_tick_time[0]
            io_tick_time[0] = current_time
            if diff.total_seconds() >= 1:
                state_control[0].state_control(current_time, trick=True)
        elif str(channel.pin) in ["GPIO25"]:
            diff = current_time - io_tick_time[1]
            io_tick_time[1] = current_time
            if diff.total_seconds() >= 1:
                state_control[1].state_control(current_time, trick=True)

        else:
            # Hard Reset
            for x in state_control:
                x.reset_state()
                x.config_loader.load_meta()
                x.config_loader.dump_config()
                x.config = x.config_loader.config
                x.cal_target()
    return


def button_release(channel, loop=None, state_control=None):
    # print('Button release :', channel)
    gpio = output_map.get(str(channel.pin))
    if gpio:
        if not channel.is_active:
            gpio.off()
    return


if __name__ == '__main__':
    print("============ Start App ===========")
    if dyn_run:
        print("============ RUN ON DYN RUN MODE ===========")
    if active_cloud:
        print("============ ACTIVE CLOUD AS {} ===========".format(platform_serial))

    loggin.log_text(BASE_DIR, 'Log target={}, actual={}\n'.format(BASE_DIR, BASE_ACTUAL))
    config_pool = [
        ConfigLoader(host=api_host, path=BASE_DIR, config_file="config1"),
        ConfigLoader(host=api_host, path=BASE_DIR, config_file="config2")
    ]

    sc_pool = [
        StateControl(config_loader=config_pool[0], logs=loggin.log_text, path=BASE_DIR,
                     version=version, state_file="state1", config_file="config1"),
        StateControl(config_loader=config_pool[1], logs=loggin.log_text, path=BASE_DIR,
                     version=version, state_file="state2", config_file="config2")
    ]

    for x in sc_pool:
        x.init_state()

    input_1.when_pressed = partial(button_press, loop=asyncio.get_event_loop(), state_control=sc_pool)
    input_1.when_released = partial(button_release, loop=asyncio.get_event_loop(), state_control=sc_pool)
    input_2.when_pressed = partial(button_press, loop=asyncio.get_event_loop(), state_control=sc_pool)
    input_2.when_released = partial(button_release, loop=asyncio.get_event_loop(), state_control=sc_pool)
    input_3.when_pressed = partial(button_press, loop=asyncio.get_event_loop(), state_control=sc_pool)
    input_3.when_released = partial(button_release, loop=asyncio.get_event_loop(), state_control=sc_pool)

    output_1.off()
    output_2.off()
    output_3.off()
    output_4.off()

    if active_cloud:
        platform.init_mqtt()

    try:
        asyncio.get_event_loop().create_task(sys_tick(sc_pool, platform, device))
        if active_cloud:
            asyncio.get_event_loop().create_task(logger_tick(sc_pool, platform, device))

        web_loop(sc_pool, platform, device, BASE_DIR)
    finally:
        for x in sc_pool:
            x.dump_state(BASE_DIR)

    print("Exit process")
