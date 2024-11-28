# -*- encoding: UTF-8 -*-

import utils
import logging
import work_flow
import settings
import schedule
import time
import datetime
from pathlib import Path

def job():
    if utils.is_weekday():
        work_flow.prepare()

logging.basicConfig(format='%(asctime)s %(message)s', filename='sequoia.log')
logging.getLogger().setLevel(logging.INFO)
settings.init()
def schedule_next_run(start_time):
    """
    调度下一个运行时间，从当前时间开始，每半个小时调度一次，直到15:00。
    """
    current_time = start_time
    while current_time.hour < 15:
        next_run_time = datetime.datetime.combine(start_time.date(), current_time)
        schedule.every(30).minutes.at(next_run_time).do(job)
        current_time = (current_time.hour * 60 + current_time.minute) // 30 * 30 // 60
        if current_time == start_time.hour:
            current_time = datetime.time(current_time.hour, 30)
        else:
            current_time = datetime.time(current_time, 0)

if settings.config['cron']:
    # 获取当前时间
    now = datetime.datetime.now()
    start_time = datetime.time(23, 15)
    end_time = datetime.time(23, 55)
    current_time = now.time()

    # 初始化schedule
    if start_time <= current_time <= end_time:
        # 如果当前时间在9:15到15:00之间，则开始调度任务
        schedule_next_run(now)

    while True:
        schedule.run_pending()
        time.sleep(1)
else:
    work_flow.prepare()

