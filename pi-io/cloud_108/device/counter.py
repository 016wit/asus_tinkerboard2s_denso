class CounterDevice(object):
    status_map = {
        "RUN": "60",
        "MEETING": "11",
        "BREAK_TIME": "80",
        "SHORT_BREAKDOWN": "21",
        "DOWN": "31"
    }

    def __init__(self, serial, *args, **kwargs):
        self.serial = serial
        self._type = 300000
        self._status = "70"
        self._machine_id = kwargs.get("machine_id", "Packing")
        self._job_id = "1234"
        self._daily_normal = 0
        self._weekly_normal = 0
        self._monthly_normal = 0
        self._yearly_normal = 0
        self._employee_id = 0
        self._target = 0
        self._target_p = 0
        self._result_p = 0
        self._pp_plan = 0
        self._actual = 0
        self._diff = 0
        self._att = 0
        self._lost_time = ''
        self._tt = 0
        return

    @property
    def type(self):
        return self._type

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value

    @property
    def machine_id(self):
        return self._machine_id

    @property
    def job_id(self):
        return self._job_id

    @property
    def daily_normal(self):
        return self._daily_normal

    @property
    def weekly_normal(self):
        return self._weekly_normal

    @property
    def monthly_normal(self):
        return self._monthly_normal

    @property
    def yearly_normal(self):
        return self._yearly_normal

    @property
    def employee_id(self):
        return self._employee_id

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, value):
        self._target = value

    @property
    def target_p(self):
        return int(self._target_p)

    @target_p.setter
    def target_p(self, value):
        self._target_p = value

    @property
    def result_p(self):
        return int(self._result_p)

    @result_p.setter
    def result_p(self, value):
        self._result_p = value

    @property
    def pp_plan(self):
        return int(self._pp_plan)

    @pp_plan.setter
    def pp_plan(self, value):
        self._pp_plan = value

    @property
    def actual(self):
        return int(self._actual)

    @actual.setter
    def actual(self, value):
        self._actual = value

    @property
    def diff(self):
        return self._diff

    @diff.setter
    def diff(self, value):
        self._diff = value

    @property
    def att(self):
        return self._att

    @att.setter
    def att(self, value):
        self._att = value

    @property
    def tt(self):
        return self._tt

    @tt.setter
    def tt(self, value):
        self._tt = value

    @property
    def lost_time(self):
        try:
            lost_time = self._lost_time.split('.')[0]
        except Exception as e:
            lost_time = '00:00:00'
        return lost_time

    @lost_time.setter
    def lost_time(self, value):
        self._lost_time = value

    def update(self, obj):
        if hasattr(obj, "result"):
            self.result_p = getattr(obj, "result", 0)
        if hasattr(obj, "actual"):
            self.actual = getattr(obj, "actual", 0)
        if hasattr(obj, "att"):
            self.att = getattr(obj, "att", 0)
        if hasattr(obj, "pp_plan"):
            self.pp_plan = getattr(obj, "pp_plan", 0)
        if hasattr(obj, "loss_time"):
            self.lost_time = getattr(obj, "loss_time", "00:00:00")
        if hasattr(obj, "target"):
            self.target = getattr(obj, "target", 0)

        if hasattr(obj, "tt"):
            self.tt = getattr(obj, "tt", 0)

        if hasattr(obj, "current_state"):
            state = getattr(obj, "current_state")
            if state == "START":
                self.status = self.status_map["MEETING"]
            else:
                self.status = self.status_map.get(state, "70")

        try:
            self._diff = self._actual - self._pp_plan
        except Exception as e:
            pass

        try:
            self._target_p = (self._actual / self._target) * 100
        except Exception as e:
            self._target_p = 0

        return

    def create_frame(self):
        return [
            self.serial,
            self.type,
            self.status,
            self.machine_id,
            self.job_id,
            self.daily_normal,
            self.weekly_normal,
            self.monthly_normal,
            self.yearly_normal,
            self.employee_id,
            self.target,
            self.target_p,
            self.result_p,
            self.pp_plan,
            self.actual,
            self.diff,
            self.att,
            self.lost_time,
            self.tt,
            0,
        ]
