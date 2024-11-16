import datetime


def get_current_time():
    return (datetime.datetime.now()).strftime("%H:%M:%S.%f")


def get_current_datetime():
    return datetime.datetime.now()


def get_current_date():
    return datetime.date.today()


def calc_timelapse(initial, final):
    init_time = datetime.datetime.strptime(initial, "%H:%M:%S.%f")
    end_time = datetime.datetime.strptime(final, "%H:%M:%S.%f")
    return str(end_time - init_time)


def get_current_timestamp_as_str_fmt() -> str:
    return datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")

def get_current_day():
    return datetime.datetime.now().date()

def get_current_hour() -> int:
    return datetime.datetime.now().hour

def get_current_datetime_for_files() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d-%H%M%S")

def get_current_datetime_for_logs() -> str:
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")   