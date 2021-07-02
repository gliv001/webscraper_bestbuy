from apscheduler.schedulers.background import BackgroundScheduler
from webscraper import bestbuy_gpu_webscraper
from fastapi import FastAPI
import asyncio
from hypercorn.asyncio import serve
from hypercorn.config import Config
import csv
import yaml

app = FastAPI()

with open("config.yml", "r") as yml:
    cfg = yaml.safe_load(yml)

@app.get('/')
@app.get('/GetAvailableGPU')
def availableGPUs():
    available_list = []
    with open(cfg["output"]["csv"], "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["Available"] == "True":
                available_list.append(row)
    return {"available_list": available_list}



if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    job = scheduler.add_job(bestbuy_gpu_webscraper, 'interval', seconds=2*60)
    scheduler.start()

    bestbuy_gpu_webscraper()
    
    asyncio.run(serve(app, Config()))