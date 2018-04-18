from application import app

from pytz import utc

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor


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

def printer():
    print("\nHello World!\n")

scheduler.start()

scheduler.add_job(printer, 'interval', seconds=15, id='my_job_id', replace_existing=True)


if __name__ == '__main__':
    app.run(debug=True)