import datetime


def work_time_format(work_t):
    r = datetime.timedelta(minutes=10)
    work_t += r
    m = 0 if work_t.minute - 30 < 0 else 30
    work_t = work_t.replace(minute=m, second=0, microsecond=0)
    return work_t
