import requests
import datetime


def or_result_test():
    dt = datetime.datetime.now()
    try:
        req = requests.post("http://{}/or_result/{}".format("localhost:5000", "AK204110107000099-01"), data={
            "datetime_stamp": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "count_val": 20,
            "pp_plan_val": 25,
            "or_val": 81.5
        })
    except Exception as e:
        print(e)
        pass

    return

def or_result_an_test():
    dt = datetime.datetime.now()
    try:
        req = requests.post("http://{}/or_analysis/{}".format("localhost:5000", "AK204110107000099-01"), data={
            "datetime_stamp": dt.strftime("%Y-%m-%dT%H:%M:%S"),
            "lost_val": 20,
            "meeting_val": 25,
            "run_val": 81,
            "down_val": 81,
            "short_breakdown_val": 81
        })
    except Exception as e:
        print(e)
        pass

    return