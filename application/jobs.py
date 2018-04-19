import os

print("\n\n{}\n\n".format("This is jobs.py"))

def printer(text="Here"):
    print("\n\n{}\n\n".format(text))

if os.environ.get("HEROKU"):
    print("\n\n{}\n\n".format("This is a heroku environment"))
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()

    @scheduler.scheduled_job('interval', minutes=2)
    def timed_job():
        print('This job is run every three minutes.')

    scheduler.start()
    scheduler.shutdown()
    scheduler.add_job(printer, 'interval', minutes=1, kwargs={"text":"This is a heroku job"})
    scheduler.start()

else:
    print("\n\n{}\n\n".format("Something happened"))

