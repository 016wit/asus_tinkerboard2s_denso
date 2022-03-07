from cloud_108 import Cloud108
from cloud_108.device import CounterDevice
from functools import reduce


def up_array(lst):
    str_txt = reduce(lambda a, b: a + str(b), lst, "")
    num = int(str_txt)
    num = num + 1

    return [int(char) for char in str(num)]


def start():
    pt = Cloud108(serial="AK204110107000099")
    df = pt.create_frame()
    device = CounterDevice("AK204110107000099-01")
    device.counter_1 = 20
    dv_f = device.create_frame()
    df = pt.fill_data(df, dv_f, 0, len(dv_f))

    # device = CounterDevice("AK204110107000099-02")
    # device.counter_1 = 20
    # dv_f = device.create_frame()
    # df = pt.fill_data(df, dv_f, 20, len(dv_f))
    #
    # device = CounterDevice("AK204110107000099-03")
    # device.counter_1 = 20
    # dv_f = device.create_frame()
    # df = pt.fill_data(df, dv_f, 40, len(dv_f))
    #
    # device = CounterDevice("AK204110107000099-04")
    # device.counter_1 = 20
    # dv_f = device.create_frame()
    # df = pt.fill_data(df, dv_f, 60, len(dv_f))
    #
    # device = CounterDevice("AK204110107000099-05")
    # device.counter_1 = 20
    # dv_f = device.create_frame()
    # df = pt.fill_data(df, dv_f, 80, len(dv_f))
    # print(df)
    result = pt.pushLog(df)
    print(result)


def push_mqtt():
    pt = Cloud108(serial="AK204110107000099")
    df = pt.create_frame()
    device = CounterDevice("AK204110107000099-01")
    device.counter_1 = 20
    dv_f = device.create_frame()
    df = pt.fill_data(df, dv_f, 0, len(dv_f))
    pt.init_mqtt()
    topic_read = "MC-01/read"
    pt.public_message(topic_read, pt.create_push_data(df))


if __name__ == '__main__':
    start()
