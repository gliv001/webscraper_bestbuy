from webscraper import bestbuy_gpu_webscraper
from emailservice import run_email_service
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(bestbuy_gpu_webscraper, "interval", seconds=60)
    job2 = scheduler.add_job(run_email_service, "interval", seconds=120)
    scheduler.start()
    try:
        while True:
            continue
    except KeyboardInterrupt:
        print("exiting..")
