from fastapi import FastAPI
from webserver.models import (
    GpuAvailability,
    SubscrbersToUrl,
    Subscribers,
    Urls,
    session as db,
)
import csv
import yaml

app = FastAPI()

with open("config.yml", "r") as yml:
    cfg = yaml.safe_load(yml)


@app.get("/GetAvailableGPU")
def availableGPUs():
    available_gpus = (
        db.query(
            GpuAvailability.name,
            GpuAvailability.model,
            GpuAvailability.sku,
            GpuAvailability.available,
            GpuAvailability.price,
            GpuAvailability.update_time,
        )
        .filter(GpuAvailability.available == True)
        .all()
    )
    return {"available_list": available_gpus}


@app.get("/GetSubscriberList")
def getSubscriberList():
    subsToUrls = (
        db.query(
            Subscribers.name,
            Subscribers.email,
            Urls.url,
            Urls.short_name,
            Urls.comment,
            SubscrbersToUrl.pattern,
        )
        .join(Subscribers)
        .join(Urls)
        .all()
    )
    return {"Subscribers": subsToUrls}


@app.get("/GetUrls")
def getUrls():
    urls = db.query(Urls.url, Urls.short_name, Urls.comment).all()
    return {"available_urls": urls}
