import os

print("\n\n{}\n\n".format("This is jobs.py"))

def printer(text="Here"):
    print("\n\n{}\n\n".format(text))

if os.environ.get("HEROKU"):
    # print("\n\n{}\n\n".format("This is a heroku environment"))
    # from apscheduler.schedulers.blocking import BlockingScheduler
    # scheduler = BlockingScheduler()

    # @scheduler.scheduled_job('interval', minutes=2)
    # def timed_job():
    #     print('This job is run every three minutes.')
    # print("\n\n{}\n\n".format("Starting a scheduler"))
    # scheduler.start()
    # print("\n\n{}\n\n".format("Scheduler started!"))
    # scheduler.shutdown()
    # scheduler.add_job(printer, 'interval', minutes=1, id="heye", kwargs={"text":"This is a heroku job"})
    
    # scheduler.start()
    
    # scheduler.print_jobs()

    from apscheduler.schedulers.background import BackgroundScheduler
    scheduler = BackgroundScheduler()

    @scheduler.scheduled_job('interval', minutes=2)
    def timed_job():
        print('This job is run every three minutes.')

    print("\n\n{}\n\n".format("Starting a scheduler"))
    scheduler.start()
    print("\n\n{}\n\n".format("Scheduler started!"))

    scheduler.add_job(printer, 'interval', minutes=1, id="heye", kwargs={"text":"This is a heroku job"})

    scheduler.print_jobs()

else:
    print("\n\n{}\n\n".format("Something happened"))

