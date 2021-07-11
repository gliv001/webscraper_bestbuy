from webscraper import bestbuy_gpu_webscraper, exit_webscraper_safely
from apscheduler.schedulers.background import BackgroundScheduler

if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(bestbuy_gpu_webscraper, "interval", seconds=60)
    scheduler.start()
    try:
        print("webscraper is running..")
        print("press ctrl+C to quit")
        bestbuy_gpu_webscraper()
        while True:
            continue
    except KeyboardInterrupt:
        print("exiting..")
        exit_webscraper_safely()
