import datetime
import os

import requests
import copy
import yaml
from .util import get_next_day

META_CONFIG = {
    "threashold": 90,
    "reset_time": "07:50:00",
    "reset_nighttime": "19:50:00",
    "cpc": "1",
    "line_name": "LINE 108ENGINEERING2 2021",
    "tt": "9.5",
    "daytime_start": "08:00:00",
    "nighttime_start": "20:00:00",
    "daytime": {
        "1": {
            "1": "10:30:00",
            "2": "10:40:00",
            "act": "on"
        },
        "2": {
            "1": "12:00:00",
            "2": "13:00:00",
            "act": "on"
        },
        "3": {
            "1": "15:05:00",
            "2": "15:35:00",
            "act": "on"
        },
        "4": {
            "1": "17:10:00",
            "2": "17:20:00",
            "act": "on"
        },
        "5": {
            "1": "17:00:01",
            "2": "17:00:02",
            "act": None
        },
        "6": {
            "1": "17:00:03",
            "2": "17:00:04",
            "act": None
        },
        "7": {
            "1": "17:00:05",
            "2": "17:00:06",
            "act": None
        },
        "8": {
            "1": "17:00:07",
            "2": "17:00:08",
            "act": None
        }
    },
    "nighttime": {
        "1": {
            "1": "22:30:00",
            "2": "22:40:00",
            "act": "on"
        },
        "2": {
            "1": "00:00:00",
            "2": "01:00:00",
            "act": "on"
        },
        "3": {
            "1": "03:05:00",
            "2": "03:30:00",
            "act": "on"
        },
        "4": {
            "1": "05:10:00",
            "2": "05:20:00",
            "act": "on"
        },
        "5": {
            "1": "05:20:01",
            "2": "05:20:02",
            "act": None
        },
        "6": {
            "1": "05:20:03",
            "2": "05:20:04",
            "act": None
        },
        "7": {
            "1": "05:20:05",
            "2": "05:20:06",
            "act": None
        },
        "8": {
            "1": "05:20:07",
            "2": "05:20:08",
            "act": None
        }
    },
    "short_break_down_threshold": 100,
    "break_down_threshold": 300,
    "meeting_threshold": 1800
}


class ConfigLoader(object):
    def __init__(self, *args, **kwargs):
        self.host = kwargs.get('host', '127.0.0.1')
        self.file_path = kwargs.get('path', '.')
        self.load_config_file = kwargs.get('config_file', 'config')
        self.config = {}
        self.load_config()

    @property
    def file_name(self):
        return self.load_config_file

    def get_config(self):
        req = requests.get('http://{}/get_config'.format(self.host))
        return req.json()

    def load_meta(self):
        dt = datetime.datetime.now()

        if os.path.exists("{}/{}_startup.yaml".format(self.file_path, self.load_config_file)):
            try:
                with open("{}/{}_startup.yaml".format(self.file_path, self.load_config_file)) as file:
                    config = yaml.full_load(file)
            except Exception as e:
                config = copy.deepcopy(META_CONFIG)
        else:
            config = copy.deepcopy(META_CONFIG)

        start_time = datetime.datetime.strptime(config["daytime_start"], '%H:%M:%S') \
            .replace(year=dt.year, month=dt.month, day=dt.day)

        reset_time = datetime.datetime.strptime(config["reset_time"], '%H:%M:%S') \
            .replace(year=dt.year, month=dt.month, day=dt.day)

        nighttime_start = datetime.datetime.strptime(config["nighttime_start"], '%H:%M:%S') \
            .replace(year=dt.year, month=dt.month, day=dt.day)

        nighttime_reset = datetime.datetime.strptime(config["reset_nighttime"], '%H:%M:%S') \
            .replace(year=dt.year, month=dt.month, day=dt.day)

        config['schedule'] = {
            'start': start_time,
            'reset': reset_time,
            'night': nighttime_start,
            'night_reset': nighttime_reset
        }

        config['break_schedule'] = [copy.deepcopy(x) for x in config['daytime'].values()] + \
                                   [copy.deepcopy(x) for x in config['nighttime'].values()]

        config['break_schedule'] = list(filter(lambda x: x['act'] == "on", config['break_schedule']))

        next_day_flag = False
        next_day = get_next_day(dt)
        last_entry = None
        for x in config['break_schedule']:
            if next_day_flag is True:
                start = datetime.datetime.strptime(x["1"], '%H:%M:%S') \
                    .replace(year=next_day.year, month=next_day.month, day=next_day.day)
                end = datetime.datetime.strptime(x["2"], '%H:%M:%S') \
                    .replace(year=next_day.year, month=next_day.month, day=next_day.day)
            else:
                start = datetime.datetime.strptime(x["1"], '%H:%M:%S') \
                    .replace(year=dt.year, month=dt.month, day=dt.day)
                end = datetime.datetime.strptime(x["2"], '%H:%M:%S') \
                    .replace(year=dt.year, month=dt.month, day=dt.day)

            # next day detect
            x['start'] = start
            x['end'] = end
            if start.hour > end.hour and next_day_flag is False:
                x['end'] = end.replace(year=next_day.year, month=next_day.month, day=next_day.day)
                next_day_flag = True
            else:
                if last_entry is not None and last_entry.hour > x['start'].hour:
                    x['start'] = start.replace(year=next_day.year, month=next_day.month, day=next_day.day)
                    x['end'] = end.replace(year=next_day.year, month=next_day.month, day=next_day.day)
                    next_day_flag = True
            last_entry = start
            del x['1']
            del x['2']

        self.config = config
        return config

    def dump_config(self):
        with open("{}/{}.yaml".format(self.file_path, self.load_config_file), 'w') as outfile:
            yaml.dump(self.config, outfile)
        return

    def load_config(self):
        if os.path.exists("{}/{}.yaml".format(self.file_path, self.load_config_file)):
            with open("{}/{}.yaml".format(self.file_path, self.load_config_file)) as file:
                self.config = yaml.full_load(file)
                return self.config
        return self.load_meta()

    def save_config(self):
        with open("{}/{}_startup.yaml".format(self.file_path, self.load_config_file), 'w') as outfile:
            yaml.dump({
                "threashold": self.config["threashold"],
                "reset_time": self.config["reset_time"],
                "reset_nighttime": self.config["reset_nighttime"],
                "cpc": self.config["cpc"],
                "line_name": self.config["line_name"],
                "tt": self.config["tt"],
                "daytime_start": self.config["daytime_start"],
                "nighttime_start": self.config["nighttime_start"],
                "daytime": self.config["daytime"],
                "nighttime": self.config["nighttime"],
                "break_down_threshold": self.config.get("break_down_threshold", 100),
                "short_break_down_threshold": self.config.get("break_down_threshold", 300),
            }, outfile)
        return
