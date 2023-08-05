# -*- coding: utf-8 -*-

# file: time_helper.py
# date: 2020-12-17


import os
from . import sys_helper
from . import log_helper
from . import num_str_helper 


logger = log_helper.get_logger(__name__)


def get_datetime_str_by_now(
        year_offset: int=0, month_offset: int=0, day_offset: int=0, 
        hour_offset: int=0, minute_offset: int=0, second_offset: int=0, 
        datetime_format: str="%Y%m%d") -> str:
    """Easyly get unix style datetime string
    Args:
        datetime_format: default "%Y%m%d", could also be "+%Y-%m-%d" etc.
    """
    output_time_str = None
    shell_cmd_temp = None

    year_offset = num_str_helper.full_num2str(year_offset)
    month_offset = num_str_helper.full_num2str(month_offset)
    day_offset = num_str_helper.full_num2str(day_offset)
    hour_offset = num_str_helper.full_num2str(hour_offset)
    minute_offset = num_str_helper.full_num2str(minute_offset)
    second_offset = num_str_helper.full_num2str(second_offset)

    if sys_helper.get_sys() == "Darwin":
        shell_cmd_temp = """
            date -v{day_offset}d -v{month_offset}m -v{year_offset}y +{dt_format}
        """
    elif sys_helper.get_sys() == "Linux":
        shell_cmd_temp = \
            """date""" + \
            """--date='{year_offset} year {month_offset} month {day_offset} day'""" + \
            """+{dt_format}"""
    else:
        logger.warning("For now `get_datetime_str_by_now` not supports {} os".format(
            sys_helper.get_sys()
        ))
        return output_time_str

    format_params = {
        "dt_format": datetime_format, 
        "year_offset": year_offset, "month_offset": month_offset, "day_offset": day_offset, 
    }
    sh_cmd = shell_cmd_temp.format(**format_params)
    return os.popen(sh_cmd).read().strip("\n")

