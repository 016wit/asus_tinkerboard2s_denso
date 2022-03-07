from datetime import datetime
from app.models import ReportStatus
from app.db import db
import calendar

key = "AK204110107000099"


def get_month_range(date):
    """
    a method use to find start date and end date of month from input date

    :param date: (:obj:`date`) or (str) The date representing the month

    :return: start date (:obj:`date`) and end date (:obj:`date`) of month
    """
    if isinstance(date, str):
        start = datetime.strptime(date, '%Y-%m-%d').date()
    else:
        start = date
    month = calendar.monthrange(start.year, start.month)
    last_date = month[1]
    start_date = start.replace(day=1)
    end_date = start.replace(day=last_date)
    return start_date, end_date


def generate_day_data(dt=datetime.now()):
    global key
    entities = []
    for i in range(24):
        for x in range(60):
            current_time = dt.replace(hour=i, minute=x, second=0)
            rs = ReportStatus(sboxName="{}-01".format(key),
                              statusValue=60,
                              userID=1,
                              datetimeStamp=str(current_time.strftime("%s")),
                              timeStampLocal=current_time,
                              dateStamp=current_time.date(),
                              timeStamp=current_time
                              )
            entities.append(rs)

    db.session.add_all(entities)
    db.session.commit()
    return entities


def generate_record(dt=datetime.now()):
    global key
    # for i in range(24):
    current_time = dt.replace(second=0)
    rs = ReportStatus(sboxName="{}-01".format(key),
                      statusValue=60,
                      userID=1,
                      datetimeStamp=str(current_time.strftime("%s")),
                      timeStampLocal=current_time,
                      dateStamp=current_time.date(),
                      timeStamp=current_time
                      )

    db.session.add(rs)
    db.session.commit()
    return


def generate_month_date(dt):
    start_date, end_date = get_month_range(dt)
    diff = end_date - start_date
    for x in range(diff.days):
        current_date = dt.replace(day=x + 1)
        generate_day_data(current_date)
        print(x + 1)


def update_record_status(start, stop, status):
    global key
    print(start, stop)
    q = ReportStatus.query.filter(ReportStatus.sboxName.startswith("AK204110107000099"),
                                  ReportStatus.timeStampLocal.between(start, stop))
    # q.update({
    #     "statusValue": 50
    # })

    for x in q:
        x.statusValue = status
    db.session.commit()
    return


def generate_demo_data_day_shift(dt, ot=False):
    update_record_status(
        dt.replace(hour=0, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=0, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=0, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=3, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=3, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=3, minute=30).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=3, minute=31).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=5, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    if ot is True:
        update_record_status(
            dt.replace(hour=5, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=5, minute=30).strftime('%Y-%m-%d %H:%M:%S'),
            51,
        )
        update_record_status(
            dt.replace(hour=5, minute=31).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=7, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
            60,
        )
    else:
        update_record_status(
            dt.replace(hour=5, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=7, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
            51,
        )
    update_record_status(
        dt.replace(hour=7, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=8, minute=59).strftime('%Y-%m-%d %H:%M:%S'),
        11,
    )
    update_record_status(
        dt.replace(hour=8, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=8, minute=10).strftime('%Y-%m-%d %H:%M:%S'),
        11
    )
    update_record_status(
        dt.replace(hour=8, minute=11).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=10, minute=20).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=10, minute=21).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=10, minute=40).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=10, minute=41).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=11, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=11, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=12, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=12, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=15, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=15, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=15, minute=30).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=15, minute=31).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=17, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )

    if ot is True:
        update_record_status(
            dt.replace(hour=17, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=17, minute=30).strftime('%Y-%m-%d %H:%M:%S'),
            51,
        )
        update_record_status(
            dt.replace(hour=17, minute=31).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=19, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
            60,
        )
    else:
        update_record_status(
            dt.replace(hour=17, minute=1).strftime('%Y-%m-%d %H:%M:%S'),
            dt.replace(hour=19, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
            51,
        )

    update_record_status(
        dt.replace(hour=19, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=20, minute=10).strftime('%Y-%m-%d %H:%M:%S'),
        11,
    )
    update_record_status(
        dt.replace(hour=20, minute=11).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=22, minute=20).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=22, minute=21).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=22, minute=40).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )
    update_record_status(
        dt.replace(hour=22, minute=41).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=23, minute=50).strftime('%Y-%m-%d %H:%M:%S'),
        60,
    )
    update_record_status(
        dt.replace(hour=23, minute=51).strftime('%Y-%m-%d %H:%M:%S'),
        dt.replace(hour=23, minute=59).strftime('%Y-%m-%d %H:%M:%S'),
        51,
    )

def create_demo_month():
    dt = datetime.now().replace(month=4, second=0)
    no_plan = [11, 18, 25]
    start_date, end_date = get_month_range(dt)
    diff = end_date - start_date
    for x in range(diff.days + 1):
        current_date = dt.replace(day=x + 1)
        if x in no_plan:
            update_record_status(
                dt.replace(hour=0, minute=0).strftime('%Y-%m-%d %H:%M:%S'),
                dt.replace(hour=23, minute=59).strftime('%Y-%m-%d %H:%M:%S'),
                51,
            )
        else:
            generate_demo_data_day_shift(current_date)
        print(x + 1)




def create_dump_state():
    # 1st may
    update_record_status("2021-04-01 08:00:00", "2021-04-02 07:59:00", 51)
    # Setting
    update_record_status("2021-04-02 08:00:00", "2021-04-02 08:30:00", 41)
    # Machine Stop
    update_record_status("2021-04-02 22:00:00", "2021-04-02 23:30:00", 31)
    update_record_status("2021-04-06 08:00:00", "2021-04-07 07:59:00", 51)
    # Other Stop  2
    update_record_status("2021-04-05 13:00:00", "2021-04-05 14:00:00", 21)
    update_record_status("2021-04-06 08:00:00", "2021-04-07 07:59:00", 51)
    # Stop Plan
    update_record_status("2021-04-10 08:00:00", "2021-04-16 07:59:00", 51)
    # Stop Plan
    update_record_status("2021-04-16 08:00:00", "2021-04-17 09:59:00", 41)
    update_record_status("2021-04-18 08:00:00", "2021-04-19 09:59:00", 41)
    update_record_status("2021-04-25 08:00:00", "2021-04-26 09:59:00", 41)

    # Machine Stop
    update_record_status("2021-04-27 18:00:00", "2021-04-27 18:59:00", 31)
    update_record_status("2021-04-27 22:00:00", "2021-04-27 22:30:00", 31)
    # Other Stop  2
    update_record_status("2021-04-27 18:00:00", "2021-04-27 18:59:00", 31)
    update_record_status("2021-04-27 22:00:00", "2021-04-27 22:30:00", 31)
