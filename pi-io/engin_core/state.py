import os
import yaml
import json
import datetime
import copy

from engin_core import common
from engin_core.line_notify import LineNotifyAgentMixIn

INIT_STATE = {
    "actual": 0,
    "result": 0,
    "pp_plan": 0,
    "att": 0,
    "loss_time": "00:00:00",
    "last_time": datetime.datetime.now(),
    "last_reset": datetime.datetime.now(),
    "graph": {},
    "break_counter": 0,
    "reset_flag": False,
    "night_reset_flag": False,
    "target": 0,
    "heart_beat": True,
    "version": "0",
    "graph_n": {},
    "uph": {},
    "or_hour": {},
}


class StateControl(LineNotifyAgentMixIn):
    def __init__(self, *args, **kwargs):
        self.state = copy.deepcopy(INIT_STATE)
        self.config_loader = kwargs.get('config_loader', None)
        assert self.config_loader is not None, 'Null config file'
        self.config = None
        self.file_path = kwargs.get('path', '.')
        self.logging = kwargs.get('logs', None)
        self.break_method = kwargs.get('break_method', 'span')
        self.version = kwargs.get('version', '1.0')
        self.load_state_file = kwargs.get('state_file', 'state')
        self.state['version'] = self.version
        self.last_event = datetime.datetime.now()
        self.current_state = "INIT"
        self.last_state = "INIT"
        self.init_state_flag = False
        self.state_counter = 0
        self.on_state_change = None
        self.tt_diff = 0
        # assert self.config is not None, 'Null config file'
        self.reset_state()

    @property
    def start_time(self):
        return self.config['schedule']['start']

    @property
    def night_time(self):
        return self.config['schedule']['night']

    @property
    def reset_time(self):
        return self.config['schedule']['reset']

    @property
    def reset_night_time(self):
        return self.config['schedule']['night_reset']

    @property
    def actual(self):
        return int(self.state.get('actual'))

    @actual.setter
    def actual(self, value):
        self.state['actual'] = value

    @property
    def result(self):
        return self.state.get('result')

    @result.setter
    def result(self, value):
        self.state['result'] = value

    @property
    def att(self):
        return self.state.get('att')

    @att.setter
    def att(self, value):
        self.state['att'] = value

    @property
    def pp_plan(self):
        return int(self.state.get('pp_plan'))

    @pp_plan.setter
    def pp_plan(self, value):
        self.state['pp_plan'] = value

    @property
    def att(self):
        return self.state.get('att')

    @att.setter
    def att(self, value):
        self.state['att'] = value

    @property
    def tt(self):
        return float(self.config.get('tt', 1))

    @property
    def cal_tt(self):
        return float(self.config.get('tt', 1)) * self.count_per_cycle

    @property
    def std_tt(self):
        return self.config.get('std_tt', 2)

    @property
    def short_break_down_threshold(self):
        return float(self.config.get('short_break_down_threshold', self.cal_tt * 2))

    @property
    def break_down_threshold(self):
        return float(self.config.get('break_down_threshold', self.cal_tt * 10))

    @property
    def meeting_threshold(self):
        return float(self.config.get('meeting_threshold', 1800))

    @property
    def loss_time(self):
        return self.state.get('loss_time')

    @loss_time.setter
    def loss_time(self, value):
        self.state['loss_time'] = value

    @property
    def last_time(self):
        return self.state.get('last_time')

    @last_time.setter
    def last_time(self, value):
        self.state['last_time'] = value

    @property
    def last_reset(self):
        return self.state.get('last_reset')

    @last_reset.setter
    def last_reset(self, value):
        self.state['last_reset'] = value

    @property
    def break_counter(self):
        return self.state.get('break_counter')

    @break_counter.setter
    def break_counter(self, value):
        self.state['break_counter'] = value

    @property
    def target(self):
        return self.state.get('target')

    @target.setter
    def target(self, value):
        self.state['target'] = value

    @property
    def heart_beat(self):
        return self.state.get('heart_beat', False)

    @heart_beat.setter
    def heart_beat(self, value):
        self.state['heart_beat'] = value

    @property
    def count_per_cycle(self):
        return int(self.config.get('cpc', 1))

    @property
    def graph_n(self):
        return self.state.get("graph_n", {})

    @property
    def uph(self):
        return self.state.get("uph", {})

    @property
    def hour_or(self):
        return self.state.get('or_hour', {})

    @property
    def service_data(self):
        dt = datetime.datetime.now()
        shift = self.get_shift(dt)
        graph_data = {}
        hour_or_data = {}
        line_graph = {}
        if shift == "day":
            offset = 8
        else:
            offset = 20

        for x in range(0, 12):
            idx = "{:02d}:00".format((x + offset) % 24)
            idx_30 = "{:02d}:30".format((x + offset) % 24)
            graph_data[idx] = self.graph_n[idx]
            hour_or_data[idx] = self.hour_or[idx]
            line_graph[idx] = self.state['graph'][idx]
            line_graph[idx_30] = self.state['graph'][idx_30]

        return {
            **self.state,
            "result": int(self.state['result']),
            "actual": int(self.state['actual']),
            "pp_plan": int(self.state['pp_plan']),
            "att": "{:.2f}".format(self.att),
            "loss_time": self.state['loss_time'].split('.')[0],
            "last_time": self.state['last_time'].strftime("%Y-%m-%d %H:%M:%S"),
            "last_reset": self.last_reset.strftime("%Y-%m-%d %H:%M:%S"),
            "diff": self.actual - self.pp_plan,
            "last_event": self.last_event.strftime("%Y-%m-%d %H:%M:%S"),
            "current_state": self.current_state,
            "last_state": self.last_state,
            "init_state_flag": self.init_state_flag,
            "state_counter": self.state_counter,
            "uph": self.get_current_uph(dt),
            "shift": self.get_shift(dt),
            "graph_data": graph_data,
            "line_graph": line_graph,
            "tt_diff": self.tt_diff
        }

    def is_idle(self, dt=datetime.datetime.now()):
        return self.reset_time <= dt < self.start_time or self.reset_night_time <= dt < self.night_time

    def is_break_time(self, dt=datetime.datetime.now()):
        for x in self.config['break_schedule']:
            if x['start'] <= dt < x['end']:
                return True
        return False

    def get_shift(self, dt=datetime.datetime.now()):
        if dt < self.night_time:
            return "day"
        return "night"

    def reset_state(self):
        self.state = copy.deepcopy(INIT_STATE)
        self.state["version"] = self.version
        for i in range(24):
            self.state['graph']["{:02d}:00".format(i)] = 0
            self.state['graph']["{:02d}:30".format(i)] = 0
            self.state['graph_n']["{:02d}:00".format(i)] = {
                "meeting": 0,
                "run": 0,
                "short_breakdown": 0,
                "down": 0,
                "break_time": 0,
                "lost": 0
            }
            self.state['uph']["{:02d}:00".format(i)] = 0
            self.state['or_hour']["{:02d}:00".format(i)] = {
                "or": 0,
                "count": 0,
                "pp_plan": 0
            }
        return

    def load_state(self, path):
        if os.path.exists("{}/{}.yaml".format(path, self.load_state_file)):
            with open("{}/{}.yaml".format(path, self.load_state_file)) as file:
                self.state = yaml.full_load(file)
                if self.state is None:
                    self.reset_state()
                else:
                    self.last_event = self.state.get("last_event", datetime.datetime.now())
                    self.current_state = self.state.get("current_state", "INIT")
                    self.last_state = self.state.get("current_state", "INIT")
                    self.init_state_flag = self.state.get("init_state_flag", False)
                    self.state_counter = self.state.get("state_counter", 0)
            if self.state is None:
                self.reset_state()
        self.state["version"] = self.version
        return

    def dump_state(self, path):
        dt = datetime.datetime.now()
        with open("{}/{}.yaml".format(path, self.load_state_file), 'w') as outfile:
            yaml.dump({
                **self.state,
                "last_event": self.last_event,
                "current_state": self.current_state,
                "last_state": self.last_state,
                "init_state_flag": self.init_state_flag,
                "state_counter": self.state_counter,
            }, outfile)
        return

    def dump_json(self, path):
        with open('{}/actual.json'.format(path), 'w') as outfile:
            json.dump({
                **self.state,
                "result": int(self.state['result']),
                "actual": int(self.state['actual']),
                "pp_plan": int(self.state['pp_plan']),
                "att": "{:.2f}".format(self.att),
                "loss_time": self.state['loss_time'].split('.')[0],
                "last_time": self.state['last_time'].strftime("%Y-%m-%d %H:%M:%S"),
            }, outfile, default=str)

    def reset_routine(self, dt):
        reset_time = self.reset_time.replace(day=dt.day, month=dt.month, year=dt.year)
        start_time = self.start_time.replace(day=dt.day, month=dt.month, year=dt.year)
        reset_night_time = self.reset_night_time.replace(day=dt.day, month=dt.month, year=dt.year)
        start_night = self.night_time.replace(day=dt.day, month=dt.month, year=dt.year)
        if callable(self.logging):
            self.logging(self.file_path, "{} : Reset routine\n".format(dt.strftime("%Y-%m-%d %H:%M:%S")))
            self.logging(self.file_path, "Check condition Time: {}  Flag: {}\n".format(reset_time < dt < start_time,
                                                                                       self.state['reset_flag']))
        if reset_time < dt < start_time:
            if self.state['reset_flag'] is False:
                if callable(self.logging):
                    self.logging(self.file_path, "{} : Reset routine\n".format(dt.strftime("%Y-%m-%d %H:%M:%S")))
                self.reset_state()
                self.config_loader.load_meta()
                self.config_loader.dump_config()
                self.config = self.config_loader.config
                self.state['reset_flag'] = True
                self.last_reset = datetime.datetime.now()
                self.cal_target(dt)
        elif reset_night_time < dt < start_night:
            if self.state['night_reset_flag'] is False:
                if callable(self.logging):
                    self.logging(self.file_path, "{} : Reset routine\n".format(dt.strftime("%Y-%m-%d %H:%M:%S")))
                self.actual = 0
                self.pp_plan = 0
                self.break_counter = 0
                self.att = 0
                self.result = 0
                self.loss_time = "00:00:00"
                self.state['night_reset_flag'] = True
        return

    def calc_pp_plan(self, dt):
        if self.get_shift(dt) == "day":
            diff = dt - self.start_time
        else:
            diff = dt - self.night_time
        if self.break_method == "span":
            total_seconds = diff.seconds + (int((diff.microseconds / 1000) / 100) / 10) - self.calc_shift(dt)
        else:
            total_seconds = diff.seconds + (int((diff.microseconds / 1000) / 100) / 10) - self.break_counter
        self.pp_plan = total_seconds / float(self.config.get('tt', 1))

        start_hour = dt.replace(minute=0, second=0, microsecond=0)
        hour_diff = dt - start_hour
        hour_shift = self.get_hour_shift(dt)
        hour_total_seconds = hour_diff.seconds + (int((hour_diff.microseconds / 1000) / 100) / 10) - hour_shift
        hour_pp_plan = 0
        hour_or = 0
        current_uph = self.get_current_uph(dt) * self.count_per_cycle
        if self.tt > 0:
            hour_pp_plan = hour_total_seconds / self.tt
            if hour_pp_plan > 0:
                hour_or = current_uph / hour_pp_plan
            else:
                hour_or = 100

        str_idx = dt.strftime("%H:00")
        self.hour_or[str_idx] = {
            "or": hour_or,
            "pp_plan": hour_pp_plan,
            "count": current_uph
        }
        return

    def calc_lost_time(self):
        total_seconds = (self.pp_plan - self.actual) * float(self.config.get('tt', 1))
        if total_seconds < 0:
            total_seconds = 0
        self.loss_time = str(datetime.timedelta(seconds=total_seconds))

        return

    def calc_operation_result(self):
        if self.pp_plan > 0:
            self.result = (self.actual / self.pp_plan) * 100
        else:
            self.result = 0
        return

    def plot_graph(self, dt):
        pick_time = common.select_pick_time(dt)
        time_idx = pick_time.strftime("%H:%M")

        self.state["graph"][time_idx] = self.result
        return

    def calc_shift(self, dt):
        second = 0
        schedule = self.get_break_schedule(dt)
        for x in schedule:
            period = x['end'] - x['start']
            if dt < x['start']:
                break
            elif x['start'] < dt <= x['end']:
                period = dt - x['start']
                second = second + period.seconds
            else:
                second += period.seconds
        return second

    def get_hour_shift(self, dt):
        second = 0
        schedule = self.get_break_schedule(dt)
        for x in schedule:
            if x['start'].hour == dt.hour and x['end'].hour == dt.hour:
                if dt >= x['end']:
                    period = x['end'] - x['start']
                    second = second + period.seconds
                elif x['start'] < dt <= x['end']:
                    period = dt - x['start']
                    second = second + period.seconds
            elif x['start'].hour == dt.hour and x['end'].hour > dt.hour:
                period = dt - x['start']
                second = second + period.seconds
            elif x['end'].hour == dt.hour and x['end'] <= dt:
                period = x['end'] - x['end'].replace(minute=0)
                second = second + period.seconds
            elif x['end'].hour == dt.hour and x['end'] >= dt:
                period = dt - x['end'].replace(minute=0)
                second = second + period.seconds
        return second

    def check_reset_routine(self):
        dt = datetime.datetime.now()
        if self.last_reset is None:
            self.last_reset = datetime.datetime.now()

        diff = dt - self.last_reset

        if diff.days >= 1:
            print("Force reset : reset routine not execute")
            self.reset_state()
            self.config_loader.load_meta()
            self.config_loader.dump_config()
            self.config = self.config_loader.config
            self.last_reset = dt

    def cal_target(self, dt=datetime.datetime.now()):
        second = 0
        total_sec = (60 * 60 * 24) / 2
        schedule = self.get_break_schedule(dt)

        if self.get_shift(dt) == "day":
            period_reset = self.start_time - self.reset_time
        else:
            period_reset = self.night_time - self.reset_night_time

        for x in schedule:
            period = x['end'] - x['start']
            second += period.seconds

        self.target = int((total_sec - second - period_reset.seconds) / self.tt)
        return

    def get_break_schedule(self, dt):
        if self.get_shift(dt) == "day":
            schedule = list(filter(lambda bt: bt['start'] < self.night_time, self.config['break_schedule']))
        else:
            schedule = list(filter(lambda bt: bt['start'] >= self.night_time, self.config['break_schedule']))
        return schedule

    def set_att(self, dt):
        diff = dt - self.last_event
        att = diff.seconds + int((diff.microseconds / 1000) / 100) / 10

        if self.count_per_cycle != 0:
            tt_diff = (self.tt * self.count_per_cycle) - att
            self.att = att / self.count_per_cycle
        else:
            tt_diff = self.tt - att
            self.att = att
        return tt_diff

    def state_control(self, dt, trick=False):
        current_time = dt
        if trick is False:
            self.heart_beat = not self.heart_beat

        if self.current_state == "INIT":
            # Pre state
            self.state_counter += 1
            # Process
            self.config_loader.load_config()
            self.config_loader.dump_config()
            self.config = self.config_loader.config
            self.load_state(self.file_path)
            self.check_reset_routine()
            self.cal_target(dt)
            self.last_event = dt
            # Finalize
            if self.is_idle(dt):
                self.change_state("IDLE", "INIT")
            elif self.last_state in ["RUN"]:
                self.change_state("RUN", "START")
            elif self.last_state in ["DOWN", "BREAK_TIME", "SHORT_BREAKDOWN"]:
                self.change_state(self.last_state, "INIT")
            else:
                self.change_state("START", "INIT")

        elif self.current_state == "IDLE":
            # Pre state
            self.reset_routine(dt)
            self.state_counter += 1
            # Process
            # Finalize
            day_start = self.start_time.replace(day=dt.day, month=dt.month, year=dt.year)
            night_start = self.night_time.replace(day=dt.day, month=dt.month, year=dt.year)
            reset_night_time = self.reset_night_time.replace(day=dt.day, month=dt.month, year=dt.year)
            start_night = self.night_time.replace(day=dt.day, month=dt.month, year=dt.year)

            if not self.is_idle(dt):
                self.last_event = dt
                if self.state['night_reset_flag'] is True or self.state['reset_flag'] is True:
                    self.state['night_reset_flag'] = False
                    self.state['reset_flag'] = False
                    self.change_state("START", "IDLE")
                elif self.last_state != "INIT":
                    self.change_state(self.last_state, "IDLE")
                elif self.last_state == "RUN" or (day_start.hour != dt.hour or night_start.hour != dt.hour):
                    self.change_state("RUN", "IDLE")
                else:
                    self.change_state("START", "IDLE")

        elif self.current_state == "START":
            # Pre state
            self.state_counter += 1
            # Process
            if trick is True:
                # calculate time from start
                if self.get_shift(dt) == "day":
                    diff = dt - self.start_time
                    start = self.start_time
                else:
                    diff = dt - self.night_time
                    start = self.night_time

                meeting_time = diff.total_seconds()
                self.set_att(dt)
                if meeting_time > 7200:
                    meeting_time = 0

                if meeting_time >= self.cal_tt:
                    total_time = meeting_time - self.cal_tt
                    self.push_graph_value(self.graph_n, "meeting", start, total_time)

                self.push_graph_value(self.graph_n, "run", dt, self.tt * self.count_per_cycle)
                self.actual += (1 * self.count_per_cycle)
                self.accumulate_uph(dt)

            self.default_routine(dt)
            # Finalize
            if trick is True:
                self.change_state("RUN", "START")
                self.last_event = dt
            else:
                time_from_start = dt - self.last_event
                total_sec = time_from_start.total_seconds()
                if total_sec >= self.meeting_threshold:
                    self.change_state("DOWN", "RUN")
                    self.push_graph_value(self.graph_n, "down", self.last_event, total_sec, acc=False)
                    self.last_event = dt

        elif self.current_state == "RUN":
            # Pre state
            self.reset_routine(dt)
            self.state_counter += 1
            total_sec = (dt - self.last_event).total_seconds()
            # Process
            if trick is True:
                tt_diff = self.set_att(dt)
                self.tt_diff = tt_diff
                self.actual += (1 * self.count_per_cycle)
                self.push_graph_value(self.graph_n, "run", dt, (self.att * self.count_per_cycle) + tt_diff, acc=True)
                if tt_diff < 0:
                    self.push_graph_value(self.graph_n, "lost", dt, (tt_diff * -1), acc=True)
                else:
                    self.pop_graph_value(self.graph_n, "lost", dt, tt_diff, max_depth=1)
                self.last_event = dt
                self.accumulate_uph(dt)

            self.default_routine(dt)
            # Finalize
            if self.is_idle(dt):
                self.change_state("IDLE", "RUN")
            elif self.is_break_time(dt):
                self.change_state("BREAK_TIME", "RUN")
            elif (total_sec + self.std_tt) > self.short_break_down_threshold:
                self.change_state("SHORT_BREAKDOWN", "RUN", total_sec)
                self.push_graph_value(self.graph_n, "short_breakdown", dt, total_sec, acc=False)

        elif self.current_state == "BREAK_TIME":
            # Pre state
            if trick is False:
                self.state_counter += 1
            # Process
            if trick is True:
                tt_diff = self.set_att(dt)
                self.actual += (1 * self.count_per_cycle)
                self.push_graph_value(self.graph_n, "run", dt, (self.att * self.count_per_cycle) + tt_diff, acc=True)
                self.pop_graph_value(self.graph_n, "break_time", dt, (self.att * self.count_per_cycle), max_depth=1)
                if tt_diff < 0:
                    self.push_graph_value(self.graph_n, "lost", dt, (tt_diff * -1), acc=True, )
                else:
                    self.pop_graph_value(self.graph_n, "lost", dt, tt_diff, max_depth=1)

                if self.last_state in ["SHORT_BREAKDOWN", "DOWN"]:
                    self.last_state = "RUN"
                self.accumulate_uph(dt)
                self.last_event = dt
            else:
                if self.is_break_time(dt):
                    self.break_counter += 1
                    self.push_graph_value(self.graph_n, "break_time", dt, 1, acc=True)

            self.default_routine(dt)
            # Finalize
            if not self.is_break_time(dt):
                self.change_state(self.last_state, "BREAK_TIME")
                self.last_event = dt

        elif self.current_state == "SHORT_BREAKDOWN":
            # Pre state
            self.reset_routine(dt)
            self.state_counter += 1
            total_sec = (dt - self.last_event).total_seconds()
            # Process
            if trick is True:
                self.set_att(dt)
                self.actual += (1 * self.count_per_cycle)
                # self.push_graph_value(self.graph_n, "run", dt, self.cal_tt)
                # self.pop_graph_value(self.graph_n, "short_breakdown", dt, self.cal_tt, max_depth=2)
                self.last_event = dt
                self.accumulate_uph(dt)
            else:
                self.push_graph_value(self.graph_n, "short_breakdown", dt, 1, acc=True)

            self.default_routine(dt)
            # Finalize
            if self.is_idle(dt):
                self.change_state("IDLE", "RUN")
            elif self.is_break_time(dt):
                self.change_state("BREAK_TIME", "SHORT_BREAKDOWN")
            elif trick is True:
                self.change_state("RUN", "SHORT_BREAKDOWN", total_sec)
            elif total_sec > self.break_down_threshold:
                self.change_state("DOWN", "SHORT_BREAKDOWN", total_sec)
                self.last_event = dt
                # self.push_graph_value(self.graph_n, "down", dt, total_sec, acc=False)
                # self.pop_graph_value(self.graph_n, "short_breakdown", dt, total_sec, max_depth=2)

        elif self.current_state == "DOWN":
            # Pre state
            # if self.init_state_flag is False and self.last_state == "SHORT_BREAKDOWN":
            #     total_sec = (dt - self.last_event).total_seconds()
            # self.pop_graph_value(self.graph_n, "short_breakdown", dt, total_sec)
            # self.push_graph_value(self.graph_n, "down", self.last_event, total_sec)
            # self.init_state_flag = True

            self.reset_routine(dt)
            self.state_counter += 1
            # Process
            if trick is True:
                self.set_att(dt)
                self.actual += (1 * self.count_per_cycle)
                # self.push_graph_value(self.graph_n, "run", dt, self.cal_tt)
                # self.pop_graph_value(self.graph_n, "down", dt, self.cal_tt)
                self.last_event = dt
                self.accumulate_uph(dt)
            else:
                self.push_graph_value(self.graph_n, "down", dt, 1, acc=True)

            self.default_routine(dt)
            # Finalize
            if self.is_idle(dt):
                self.change_state("IDLE", "DOWN")
            elif self.is_break_time(dt):
                self.change_state("BREAK_TIME", "DOWN")
            elif trick is True:
                self.change_state("RUN", "DOWN", self.state_counter)

        self.last_time = current_time

    def change_state(self, next_state, current_state, duration=0):
        self.current_state = next_state
        self.last_state = current_state
        self.state_counter = 0
        self.init_state_flag = False
        if callable(self.on_state_change):
            self.on_state_change(next_state, current_state)
        # self.line_notify("State Change : {} -> {}\n Duration : {} sec".format(current_state, next_state, duration))

    def init_state(self, dt=datetime.datetime.now()):
        self.change_state('INIT', 'INIT')
        self.reset_state()
        self.state_control(dt)

    def default_routine(self, dt):
        self.calc_pp_plan(dt)
        self.calc_lost_time()
        self.calc_operation_result()
        self.plot_graph(dt)

    def pop_graph_value(self, obj, key, dt, total_sec, depth=0, max_depth=2):
        if depth >= max_depth:
            return
        idx = dt.replace(minute=0)
        str_idx = idx.strftime("%H:%M")
        data_obj = obj.get(str_idx, None)

        if data_obj is None:
            return

        current_value = data_obj.get(key, 0)
        if current_value >= total_sec:
            data_obj[key] = current_value - total_sec
        else:
            data_obj[key] = 0
            remain = total_sec - current_value
            next_hour = dt.hour - 1 if dt.hour > 0 else 23
            next_time_idx = dt.replace(hour=next_hour, minute=0)
            return self.pop_graph_value(obj, key, next_time_idx, remain, depth=depth + 1, max_depth=max_depth)

        return

    def push_graph_value(self, obj, key, dt, total_sec, acc=False):
        idx = dt.replace(minute=0)
        str_idx = idx.strftime("%H:%M")
        data_obj = obj.get(str_idx, None)

        max_value = (60 - dt.minute) * 60
        if acc is False:
            max_value = 3600

        if data_obj is None:
            obj[str_idx] = {
                "meeting": 0,
                "run": 0,
                "short_breakdown": 0,
                "down": 0,
                "break_time": 0,
                "lost": 0
            }
            data_obj = obj[str_idx]

        if total_sec > max_value:
            if acc:
                remain = total_sec - max_value
                data_obj[key] += max_value
            else:
                remain = total_sec - max_value
                data_obj[key] = max_value

            next_idx = dt.replace(hour=((dt.hour + 1) % 24), minute=0)
            return self.push_graph_value(obj, key, next_idx, remain)
        else:
            if acc:
                data_obj[key] += total_sec
            else:
                data_obj[key] = total_sec
        return

    def accumulate_uph(self, dt):
        idx = dt.replace(minute=0)
        str_idx = idx.strftime("%H:00")
        if str_idx in self.uph:
            self.uph[str_idx] += (1 * self.count_per_cycle)
        else:
            self.uph[str_idx] = 1 * self.count_per_cycle
        return self.uph[str_idx]

    def get_current_uph(self, dt):
        idx = dt.replace(minute=0)
        str_idx = idx.strftime("%H:00")
        return self.uph.get(str_idx, 0)
