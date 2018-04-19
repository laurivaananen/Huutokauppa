import os

def printer(text="Here"):
    print("\n\n{}\n\n".format(text))

if os.environ.get("HEROKU"):
    from apscheduler.schedulers.blocking import BlockingScheduler
    scheduler = BlockingScheduler()

    scheduler.start()
    scheduler.add_job(printer, 'interval', minutes=1, kwargs={"text":"This is a heroku job"})

