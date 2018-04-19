import os

def printer(text="Here"):
    print("\n\n{}\n\n".format(text))

if os.environ.get("HEROKU"):
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()

    # @scheduler.scheduled_job('interval', minutes=3)
    # def timed_job():
    #     print('This job is run every three minutes.')

    # @scheduler.scheduled_job('cron', day_of_week='mon-fri', hour=17)
    # def scheduled_job():
    #     print('This job is run every weekday at 5pm.')

    scheduler.start()
    scheduler.add_job(printer, 'interval', minutes=1, replace_existing=True, kwargs={"text":"This is a heroku job"})

else:
    from application import scheduler
    scheduler.add_job(printer, 'interval', minutes=1, replace_existing=True, id="Original_id", kwargs={"text":"This is a heroku job"})
