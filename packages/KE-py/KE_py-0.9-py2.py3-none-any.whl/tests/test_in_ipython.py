# coding=u8
import sys
from KE import KE
from KE.v3.segments import Segments
import time
from datetime import date, datetime, timedelta
import calendar
from KE.client import KE4CONF as CONF


# 输入KE实例的HOST；PORT；USERNAME；PASSWORD
client = KE(CONF['host'], port=CONF['port'], username=CONF['username'], password=CONF['password'], version=4, debug=True)


def check_current_job_num():
    """
    获取当前在跑的任务数
    :return:
    """
    jobs = client.jobs(status=2)
    return len(jobs)


def check_job_staus(job_id):
    job = client.jobs(key=job_id)[0]
    return job


def build(model, start_time, end_time):
    start_time = datetime.strptime(start_time, '%Y%m%d')
    end_time = datetime.strptime(end_time, '%Y%m%d')
    start_time = start_time + timedelta(hours=8)
    end_time = end_time + timedelta(hours=8)
    job = model.build(start_time=start_time, end_time=end_time)
    print(job)
    job_id = job['data']['jobs'][0]['job_id']

    while True:
        job = check_job_staus(job_id)
        status = job.status
        if status in ['PENDING', 'RUNNING']:
            print('Please wait, Job status: %s' % status)
            time.sleep(60)
        else:
            print(status)
            break


if __name__ == '__main__':
    """
    运行方式：
    python build_segment_4x.py 20200101 20200102 kylin_sales_cube
    """
    start_time = sys.argv[1]
    end_time = sys.argv[2]
    project = sys.argv[3].strip()
    model = sys.argv[4].strip()

    model = client.models(name=model, project=project)[0]
    build(model, start_time, end_time)


