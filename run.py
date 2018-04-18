from application import app

from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor

from datetime import datetime


jobstores = {
    'default': SQLAlchemyJobStore(url='sqlite:///jobs.db')
}
executors = {
    'default': ThreadPoolExecutor(20),
    'processpool': ProcessPoolExecutor(5)
}
job_defaults = {
    'coalesce': False,
    'max_instances': 3
}
scheduler = BackgroundScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone=utc)


def printer(text):
    print("\n{}\n".format(text))

scheduler.start()

scheduler.add_job(printer, 'date', run_date=datetime(2018, 4, 18, 15, 38, 20, 0, utc), id='my_job_id', replace_existing=True, kwargs={"text":"HelloWOrld"})


if __name__ == '__main__':
    app.run(debug=False)