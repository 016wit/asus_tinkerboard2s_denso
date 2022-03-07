import os
import json
import yaml
import subprocess
from functools import partial
import aiohttp_cors
from aiohttp import web


async def handle(request, state_control=None, platform=None, devices=None, *args, **kwargs):
    return web.json_response({
        "result": "OK"
    })


async def handle_state(request, state_control=None, platform=None, devices=None, *args, **kwargs):
    if request.method == 'PUT':
        select = int(request.query.get('select', None))
        body = await request.json()
        if "data" in body and select in [0, 1]:
            state_control[select].actual = body["data"]
            print("Update request force actual : -> {}".format(state_control[select].actual))
    else:
        all_data = []
        for x in state_control:
            all_data.append(x.service_data)
        return web.json_response({
            "result": "OK",
            "data": all_data
        })
    return web.json_response({
        "result": "OK"
    })


async def handle_system(request, state_control=None, platform=None, devices=None, *args, **kwargs):
    body = await request.json()
    if "time" in body:
        request_time = body.get("time", None)
        print(request_time)
        subprocess.Popen("date -s \"{}\"".format(request_time), shell=True, stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen("hwclock -w", shell=True, stdout=subprocess.PIPE).communicate()[0]
        subprocess.Popen("hwclock -s", shell=True, stdout=subprocess.PIPE).communicate()[0]

    return web.json_response({
        "result": "OK"
    })


async def handle_config(request, state_control=None, platform=None, devices=None, file_path='.', *args, **kwargs):
    if request.method == 'PUT':
        topic = request.query.get('type', None)
        body = await request.json()
        if topic == "system":
            with open("{}/system_config.yaml".format(file_path), 'w') as outfile:
                yaml.dump(body, outfile)
        elif topic == "ins":
            select = request.query.get('select', None)
            if select is not None:
                sc = state_control[int(select)]
                print(sc.config_loader.file_name, "{}/{}_startup.yaml".format(file_path, sc.config_loader.file_name))

                with open("{}/{}_startup.yaml".format(file_path, sc.config_loader.file_name), 'w') as outfile:
                    yaml.dump(body, outfile)

                new_config = sc.config_loader.load_meta()
                sc.config_loader.dump_config()
                sc.config = new_config
                sc.cal_target()
    else:
        all_data = []
        if request.query.get('loader', None):
            for x in state_control:
                data = json.dumps(x.config_loader.config, default=str)
                all_data.append(json.loads(data))
        else:
            for x in state_control:
                data = json.dumps(x.config, default=str)
                all_data.append(json.loads(data))

        if os.path.exists("{}/system_config.yaml".format(file_path)):
            with open("{}/system_config.yaml".format(file_path)) as file:
                config = yaml.full_load(file)
        else:
            config = {
                "line_name": "LINE01",
                "switch_time": 10,
            }

        return web.json_response({
            "result": "OK",
            "system": config,
            "data": all_data
        })

    return web.json_response({
        "result": "OK",
    })


async def handle_dyn_run(request, state_control=None, platform=None, devices=None, *args, **kwargs):
    device = int(request.query.get('dev', None))
    rsp = {}
    if device in [0, 1] and state_control is not None:
        state_control[device].calculate_result()
        rsp = state_control[device].service_data

    return web.json_response({
        "result": "OK",
        "state": rsp
    })


async def handle_reboot(request, *args, **kwargs):
    if request.method == 'POST':
        subprocess.Popen("reboot", shell=True, stdout=subprocess.PIPE).communicate()[0]


def web_loop(state_obj, pt=None, dev=None, file_path='.', on_start_up=None, ):
    app = web.Application()
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
            allow_methods=["GET", "POST", "PUT", "OPTIONS"]
        )
    })

    app.router.add_route("GET", "/", partial(handle, state_control=state_obj, platform=pt, devices=dev))
    app.router.add_route("GET", "/state", partial(handle_state, state_control=state_obj, platform=pt, devices=dev))
    app.router.add_route("PUT", "/state", partial(handle_state, state_control=state_obj, platform=pt, devices=dev))

    app.router.add_route("GET", "/config",
                         partial(handle_config, state_control=state_obj, platform=pt, devices=dev, file_path=file_path))
    app.router.add_route("PUT", "/config",
                         partial(handle_config, state_control=state_obj, platform=pt, devices=dev, file_path=file_path))

    app.router.add_route("PUT", "/dyn_run", partial(handle_dyn_run, state_control=state_obj, platform=pt, devices=dev))

    app.router.add_route("PUT", "/set_time", partial(handle_system, state_control=state_obj, platform=pt, devices=dev))
    app.router.add_route("POST", "/reboot", partial(handle_reboot, state_control=state_obj, platform=pt, devices=dev))

    for route in list(app.router.routes()):
        cors.add(route)
    print("File", file_path)
    print("======= Serving on http://127.0.0.1:8080/ ======")
    if callable(on_start_up):
        app.on_startup.append(on_start_up)
    web.run_app(app)
    print("======= END TASK  ======")
