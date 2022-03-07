import unittest
from datetime import datetime
from engin_core import StateControl
from engin_core import ConfigLoader


class TestStateControl(unittest.TestCase):
    def setUp(self) -> None:
        self.config_loader = ConfigLoader()
        self.state_control = StateControl(config_loader=self.config_loader)

    def setup_config(self):
        self.state_control.config_loader.load_config()
        self.state_control.config = self.config_loader.config
        dt = datetime.now()
        self.state_control.config["tt"] = 10
        self.state_control.config['schedule']['reset'] = dt.replace(hour=7, minute=50, second=0, microsecond=0)
        self.state_control.config['schedule']['start'] = dt.replace(hour=8, minute=0, second=0, microsecond=0)

    def test_graph_n(self):
        """
            Test State control init normalize graph
        """
        time_idx = ["{:02d}:00".format(x) for x in range(24)]
        self.assertCountEqual(time_idx, self.state_control.graph_n.keys())
        for x in time_idx:
            self.assertIn(x, self.state_control.graph_n)
            self.assertIn("meeting", self.state_control.graph_n[x])
            self.assertIn("run", self.state_control.graph_n[x])
            self.assertIn("short_breakdown", self.state_control.graph_n[x])
            self.assertIn("down", self.state_control.graph_n[x])
            self.assertIn("break_time", self.state_control.graph_n[x])
            self.assertIn("lost", self.state_control.graph_n[x])

    def test_push_graph_value_acc_mode(self):
        """
            Test State control push_graph_value function accumulate mode
        """
        dt = datetime.now().replace(hour=8, minute=20)
        sc = self.state_control
        sc.push_graph_value(sc.graph_n, "run", dt, 20)
        self.assertEqual(20, sc.graph_n['08:00']['run'], "Run time must equal 20")
        sc.push_graph_value(sc.graph_n, "run", dt, 20, acc=True)
        self.assertEqual(40, sc.graph_n['08:00']['run'], "Run time must equal 40")
        sc.push_graph_value(sc.graph_n, "run", dt, 0, acc=False)
        sc.push_graph_value(sc.graph_n, "run", dt, 3600, acc=True)
        self.assertEqual(2400, sc.graph_n['08:00']['run'], "Run time must equal 2400")
        self.assertEqual(1200, sc.graph_n['09:00']['run'], "Run time must equal 1200")
        dt = datetime.now().replace(hour=12, minute=30)
        sc.push_graph_value(sc.graph_n, "run", dt, 7500, acc=True)
        self.assertEqual(1800, sc.graph_n['12:00']['run'], "Run time must equal 1600")
        self.assertEqual(3600, sc.graph_n['13:00']['run'], "Run time must equal 3600")
        self.assertEqual(2100, sc.graph_n['14:00']['run'], "Run time must equal 2100")

    def test_push_graph_if_next_is_zero_acc_mode(self):
        """
            Test State control push_graph_value function
            condition next index is zero
        """
        dt = datetime.now().replace(hour=23, minute=0)
        sc = self.state_control
        sc.push_graph_value(sc.graph_n, "run", dt.replace(hour=23, minute=0), 3800, acc=True)
        self.assertEqual(3600, sc.graph_n['23:00']['run'], "Run time must equal 3600")
        self.assertEqual(200, sc.graph_n['00:00']['run'], "Run time must equal 200")

    def test_push_graph_value_static_mode(self):
        """
            Test State control push_graph_value function static mode
        """
        dt = datetime.now().replace(hour=8, minute=20)
        sc = self.state_control
        sc.push_graph_value(sc.graph_n, "run", dt, 120, acc=False)
        self.assertEqual(120, sc.graph_n['08:00']['run'], "Run time must equal 120")
        sc.push_graph_value(sc.graph_n, "run", dt, 60, acc=False)
        self.assertEqual(60, sc.graph_n['08:00']['run'], "Run time must equal 60")
        sc.push_graph_value(sc.graph_n, "run", dt, 60, acc=False)
        dt = datetime.now().replace(hour=12, minute=50)
        sc.push_graph_value(sc.graph_n, "run", dt, 4500, acc=False)
        self.assertEqual(3600, sc.graph_n['12:00']['run'], "Run time must equal 3600")
        self.assertEqual(900, sc.graph_n['13:00']['run'], "Run time must equal 900")
        sc.push_graph_value(sc.graph_n, "run", dt, 7500, acc=False)
        self.assertEqual(3600, sc.graph_n['12:00']['run'], "Run time must equal 3600")
        self.assertEqual(3600, sc.graph_n['13:00']['run'], "Run time must equal 3600")
        self.assertEqual(300, sc.graph_n['14:00']['run'], "Run time must equal 300")

    def test_pop_graph_value(self):
        """
            Test State control test_pop_graph_value function
        """
        sc = self.state_control
        dt = datetime.now().replace(hour=8, minute=0)
        sc.push_graph_value(sc.graph_n, "run", dt, 120, acc=False)
        sc.pop_graph_value(sc.graph_n, "run", dt, 60)
        self.assertEqual(60, sc.graph_n['08:00']['run'], "Run time must equal 60")
        dt = datetime.now().replace(hour=7, minute=0)
        sc.push_graph_value(sc.graph_n, "run", dt, 120, acc=False)
        dt = datetime.now().replace(hour=8, minute=0)
        sc.pop_graph_value(sc.graph_n, "run", dt, 120)
        self.assertEqual(0, sc.graph_n['08:00']['run'], "Run time must equal 0")
        self.assertEqual(60, sc.graph_n['07:00']['run'], "Run time must equal 60")

    def test_pop_graph_value_if_current_is_zero(self):
        """
            Test State control test_pop_graph_value function static mode
        """
        sc = self.state_control
        dt = datetime.now().replace(hour=0, minute=0)
        sc.push_graph_value(sc.graph_n, "run", dt, 60, acc=False)
        sc.push_graph_value(sc.graph_n, "run", dt.replace(hour=23), 120, acc=False)
        sc.pop_graph_value(sc.graph_n, "run", dt, 80)
        self.assertEqual(100, sc.graph_n['23:00']['run'], "Run time must equal 100")
        self.assertEqual(0, sc.graph_n['00:00']['run'], "Run time must equal 0")

    def test_set_att(self):
        """
            Test State control set_att function
        """
        sc = self.state_control
        sc.init_state()
        dt = datetime.now().replace(hour=0, minute=0, second=31)
        sc.config['tt'] = 10
        sc.config['cpc'] = 1
        sc.last_event = dt.replace(second=20)
        diff = sc.set_att(dt)
        self.assertEqual(11, sc.att, "ATT must equal 11")
        self.assertEqual(-1, diff, "Lost time must equal -1")
        sc.config['cpc'] = 2
        dt = datetime.now().replace(hour=0, minute=0, second=44)
        diff = sc.set_att(dt)
        self.assertEqual(12, sc.att, "ATT must equal 12")
        self.assertEqual(-4, diff, "Lost time must equal -2")
        dt = datetime.now().replace(hour=0, minute=0, second=38)
        diff = sc.set_att(dt)
        self.assertEqual(9, sc.att, "ATT must equal 9")
        self.assertEqual(2, diff, "Lost time must equal 2")

    def test_init_state(self):
        """
            Test State control init state function
        """
        self.assertEqual(self.state_control.current_state, "INIT")
        self.assertEqual(self.state_control.last_state, "INIT")
        self.assertEqual(self.state_control.state_counter, 0)

    def test_init_state_jump_to_start(self):
        """
            Test State control init state function and jump to START STATE
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=8, minute=0, second=0)
        sc.init_state(dt)
        self.assertEqual(self.state_control.current_state, "START")

    def test_init_state_jump_to_idle(self):
        """
            Test State control init state function
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now()
        sc.init_state(dt.replace(hour=7, minute=55, second=0))
        self.assertEqual(self.state_control.current_state, "IDLE")
        sc.state_control(dt.replace(hour=19, minute=52, second=0), trick=False)
        self.assertEqual(self.state_control.current_state, "IDLE")

    def test_state_control_start_state(self):
        """
            Test State control state_control function
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        sc.init_state(dt)
        self.assertEqual(self.state_control.current_state, "START")
        dt = datetime.now().replace(hour=8, minute=10, second=0, microsecond=0)
        self.state_control.config["tt"] = 10
        sc.state_control(dt, trick=True)
        self.assertEqual(self.state_control.last_state, "START")
        self.assertEqual(self.state_control.current_state, "RUN")
        self.assertEqual(590, sc.graph_n['08:00']['meeting'], "Meeting time must equal 590")
        self.assertEqual(10, sc.graph_n['08:00']['run'], "Run time must equal 10")
        self.assertEqual(1, sc.actual, "Actual must equal 1")
        self.assertEqual(dt, sc.last_event, "last_event must equal dt")

    def test_state_control_run_state(self):
        """
            Test State control state_control function
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        sc.init_state(dt)
        self.state_control.config["cpc"] = 1
        self.state_control.config["tt"] = 10
        dt = datetime.now().replace(hour=8, minute=5, second=0)
        sc.state_control(dt, trick=True)
        self.assertEqual(self.state_control.current_state, "RUN")
        self.assertEqual(10, sc.graph_n['08:00']['run'], "Run time must equal 10")
        self.assertEqual(0, sc.graph_n['08:00']['lost'], "Lost time must equal 0")
        sc.state_control(dt.replace(second=11), trick=True)
        self.assertEqual(20, sc.graph_n['08:00']['run'], "Run time must equal 20")
        self.assertEqual(1, sc.graph_n['08:00']['lost'], "Lost time must equal 1")
        sc.state_control(dt.replace(second=22), trick=True)
        self.assertEqual(30, sc.graph_n['08:00']['run'], "Run time must equal 30")
        self.assertEqual(2, sc.graph_n['08:00']['lost'], "Run time must equal 2")
        self.assertEqual(self.state_control.current_state, "RUN")
        sc.state_control(dt.replace(second=32), trick=True)
        self.assertEqual(40, sc.graph_n['08:00']['run'], "Run time must equal 40")
        self.assertEqual(2, sc.graph_n['08:00']['lost'], "Run time must equal 2")
        sc.state_control(dt.replace(second=41), trick=True)
        self.assertEqual(50, sc.graph_n['08:00']['run'], "Run time must equal 50")
        self.assertEqual(1, sc.graph_n['08:00']['lost'], "Run time must equal 1")
        self.assertEqual(self.state_control.current_state, "RUN", "State must be RUN")

    def test_state_control_run_state_to_idle_state(self):
        """
            Test State control state_control function
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=7, minute=49, second=0, microsecond=0)
        sc.last_event = dt
        sc.current_state = "RUN"
        sc.config["short_break_down_threshold"] = 600
        sc.state_control(dt.replace(second=40), trick=True)
        self.assertEqual(self.state_control.current_state, "RUN", "State must be RUN")
        sc.state_control(dt.replace(second=55), trick=True)
        self.assertEqual(self.state_control.current_state, "RUN", "State must be RUN")
        sc.state_control(dt.replace(minute=50, second=0), trick=False)
        self.assertEqual(self.state_control.current_state, "IDLE", "State must be IDLE")
        self.assertEqual(20, sc.graph_n['07:00']['run'], "Run time must equal 20")
        sc.graph_n['06:00']['run'] = 99999
        sc.state_control(dt.replace(minute=55, second=0), trick=False)
        self.assertEqual(self.state_control.current_state, "IDLE", "State must be IDLE")
        self.assertEqual(0, sc.graph_n['07:00']['lost'], "Run time must equal 0")
        self.assertEqual(0, sc.graph_n['06:00']['run'], "Run time must equal 0")
        sc.state_control(dt.replace(hour=8, minute=0, second=0), trick=False)
        self.assertEqual(self.state_control.current_state, "START", "State must be START")
        self.assertEqual(self.state_control.last_event.strftime("%H:%M"), "08:00", "State last event must be 08:00")

    def test_state_control_run_state_to_break_time_state(self):
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=10, minute=40, second=0, microsecond=0)
        sc.graph_n['10:00']['run'] = 2000
        sc.current_state = "RUN"
        sc.last_event = dt.replace(hour=10, minute=29, second=55)
        sc.state_control(dt.replace(hour=10, minute=30, second=0), trick=False)
        self.assertEqual(self.state_control.current_state, "BREAK_TIME", "State must be BREAK_TIME")
        sc.state_control(dt.replace(hour=10, minute=30, second=10), trick=True)
        self.assertEqual(2010, sc.graph_n['10:00']['run'], "Run time must equal 2010")
        self.assertEqual(self.state_control.current_state, "BREAK_TIME", "State must be BREAK_TIME")
        sc.state_control(dt.replace(hour=10, minute=35, second=0), trick=False)
        sc.state_control(dt.replace(hour=10, minute=35, second=2), trick=False)
        self.assertEqual(self.state_control.current_state, "BREAK_TIME", "State must be BREAK_TIME")
        self.assertEqual(2, sc.graph_n['10:00']['break_time'], "Break time must equal 2")
        sc.state_control(dt.replace(hour=10, minute=40, second=0), trick=False)
        self.assertEqual(2, sc.graph_n['10:00']['break_time'], "Break time must equal 2")
        self.assertEqual(self.state_control.current_state, "RUN", "State must be RUN")
        self.assertEqual(2010, sc.graph_n['10:00']['run'], "Run time must equal 2010")

    def test_state_control_run_state_to_short_breakdown_state(self):
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        sc.last_event = dt
        sc.config["short_break_down_threshold"] = 40
        sc.change_state("RUN", "IDLE")
        sc.state_control(dt.replace(hour=9, minute=0, second=30), trick=False)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(sc.current_state, "RUN", "State must be RUN")
        sc.state_control(dt.replace(hour=9, minute=0, second=40), trick=False)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(40, sc.graph_n['09:00']['short_breakdown'], "Run time must equal 40")
        self.assertEqual(sc.current_state, "SHORT_BREAKDOWN", "State must be SHORT_BREAKDOWN")
        sc.state_control(dt.replace(hour=9, minute=1, second=45), trick=True)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(40, sc.graph_n['09:00']['short_breakdown'], "Run time must equal 40")
        self.assertEqual(sc.current_state, "RUN", "State must be RUN")

    def test_state_control_run_state_to_down_state(self):
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        sc.last_event = dt
        sc.config["short_break_down_threshold"] = 40
        sc.config["break_down_threshold"] = 120
        sc.change_state("RUN", "IDLE")

        sc.state_control(dt.replace(hour=9, minute=0, second=30), trick=False)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(sc.current_state, "RUN", "State must be RUN")

        sc.state_control(dt.replace(hour=9, minute=0, second=40), trick=False)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(40, sc.graph_n['09:00']['short_breakdown'], "Run time must equal 40")
        self.assertEqual(sc.current_state, "SHORT_BREAKDOWN", "State must be SHORT_BREAKDOWN")

        sc.state_control(dt.replace(hour=9, minute=2, second=20), trick=False)
        self.assertEqual(0, sc.graph_n['09:00']['down'], "DOWN time must equal 0")
        sc.state_control(dt.replace(hour=9, minute=2, second=21), trick=False)
        self.assertEqual(1, sc.graph_n['09:00']['down'], "DOWN time must equal 1")
        self.assertEqual(sc.current_state, "DOWN", "State must be DOWN")

        for x in range(1, 20):
            sc.state_control(dt.replace(hour=9, minute=2, second=20 + x), trick=False)
        self.assertEqual(20, sc.graph_n['09:00']['down'], "DOWN time must equal 20")
        self.assertEqual(sc.current_state, "DOWN", "State must be DOWN")

        sc.state_control(dt.replace(hour=9, minute=2, second=45), trick=True)
        self.assertEqual(0, sc.graph_n['09:00']['run'], "Run time must equal 0")
        self.assertEqual(20, sc.graph_n['09:00']['down'], "Run time must equal 20")
        self.assertEqual(sc.current_state, "RUN", "State must be RUN")

    def test_get_uph(self):
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=9, minute=0, second=0, microsecond=0)
        sc.last_event = dt
        sc.accumulate_uph(dt)
        self.assertEqual(1, sc.uph['09:00'], "UPH  must equal 1")

    def test_meeting_time_ignore(self):
        """
            Scenario Meeting time will be ignore if first event be active 2 hour later
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=7, minute=55, second=0, microsecond=0)
        sc.last_event = dt
        sc.change_state("IDLE", "INIT")
        sc.state_control(dt, trick=False)
        self.assertEqual(sc.current_state, "IDLE", "State must be IDLE")
        self.assertEqual(sc.last_event.strftime("%H:%M"), "07:55", "State last event must be 07:55")

        sc.state_control(dt.replace(hour=8, minute=0), trick=False)
        self.assertEqual(sc.current_state, "START", "State must be START")
        self.assertEqual(sc.last_event.strftime("%H:%M"), "08:00", "State last event must be 08:00")

        self.state_control.config["tt"] = 10
        sc.state_control(dt.replace(hour=12, minute=0), trick=True)
        self.assertEqual(sc.current_state, "RUN", "State must be RUN")
        self.assertEqual(sc.last_event.strftime("%H:%M"), "12:00", "State last event must be 12:00")
        self.assertEqual(0, sc.graph_n['08:00']['meeting'], "Meeting time must equal 0")
        self.assertEqual(0, sc.graph_n['09:00']['meeting'], "Meeting time must equal 0")
        self.assertEqual(0, sc.graph_n['12:00']['meeting'], "Meeting time must equal 0")
        self.assertEqual(10, sc.graph_n['12:00']['run'], "Run time must equal 0")

    def test_run_time_with_cpc(self):
        """
            Scenario run time and lost time will store with real data (With multiple counter per cycle
        """
        sc = self.state_control
        self.setup_config()
        dt = datetime.now().replace(hour=8, minute=0, second=0, microsecond=0)
        sc.config['tt'] = 3
        sc.config['cpc'] = 4
        sc.last_event = dt
        sc.change_state("RUN", "START")
        dt = dt.replace(second=dt.second + 14)
        sc.state_control(dt, trick=True)
        self.assertEqual(12, sc.graph_n['08:00']['run'], "Meeting time must equal 12")
        self.assertEqual(2, sc.graph_n['08:00']['lost'], "Meeting time must equal 2")

    def test_cal_calculate_break_time_by_hour(self):
        """
             Get total breaktime in 22:30 to 22:40
         """
        sc = self.state_control
        self.setup_config()
        sc.config['tt'] = 10
        dt = datetime.now().replace(hour=22, minute=59, second=0, microsecond=0)
        shift = sc.get_hour_shift(dt)
        self.assertEqual(600, shift, "Shift time must equal 300")
        sc.config['break_schedule'][1]['start'] = sc.config['break_schedule'][1]['start'].replace(hour=11, minute=50)
        sc.config['break_schedule'][1]['end'] = sc.config['break_schedule'][1]['start'].replace(hour=12, minute=50)
        dt = datetime.now().replace(hour=12, minute=0, second=0, microsecond=0)
        shift = sc.get_hour_shift(dt)
        self.assertEqual(0, shift, "Shift time must equal 0")
        shift = sc.get_hour_shift(dt.replace(minute=1))
        self.assertEqual(60, shift, "Shift time must equal 60")
        shift = sc.get_hour_shift(dt.replace(minute=20))
        self.assertEqual(60 * 20, shift, "Shift time must equal 1200")
        shift = sc.get_hour_shift(dt.replace(hour=11, minute=55))
        self.assertEqual(60 * 5, shift, "Shift time must equal 300")

    def test_break_time_reach(self):
        sc = self.state_control
        self.setup_config()
        sc.config['meeting_threshold'] = 1800
        dt = datetime.now().replace(hour=8, minute=30, second=0, microsecond=0)
        sc.last_event = dt.replace(minute=0)
        sc.change_state("START", "IDLE")
        sc.state_control(dt, trick=False)
        self.assertEqual(1800, sc.graph_n['08:00']['down'], "DOWN time must equal 1800")
        sc.last_event = dt.replace(minute=0)
        sc.change_state("START", "IDLE")
        sc.state_control(dt.replace(minute=50), trick=False)
        self.assertEqual(3000, sc.graph_n['08:00']['down'], "DOWN time must equal 3000")
        sc.last_event = dt.replace(minute=0)
        sc.change_state("START", "IDLE")
        sc.state_control(dt.replace(hour=9, minute=10), trick=False)
        self.assertEqual(3600, sc.graph_n['08:00']['down'], "DOWN time must equal 3600")
        self.assertEqual(600, sc.graph_n['09:00']['down'], "DOWN time must equal 600")
        sc.last_event = dt.replace(hour=8, minute=0)
        sc.change_state("START", "IDLE")
        sc.state_control(dt.replace(hour=10, minute=10), trick=False)
        self.assertEqual(3600, sc.graph_n['08:00']['down'], "DOWN time must equal 3600")
        self.assertEqual(3600, sc.graph_n['09:00']['down'], "DOWN time must equal 3600")
        self.assertEqual(600, sc.graph_n['10:00']['down'], "DOWN time must equal 600")


if __name__ == '__main__':
    unittest.main(verbosity=2)
