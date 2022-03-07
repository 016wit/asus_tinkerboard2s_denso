def get_next_day(current_date):
    try:
        dt = current_date.replace(day=current_date.day + 1)
    except Exception as e:
        try:
            dt = current_date.replace(day=1, month=current_date.month + 1)
        except Exception as e:
            dt = current_date.replace(day=1, month=1, year=current_date.year + 1)
    return dt
