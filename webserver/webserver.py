from fastapi import FastAPI
from db import (
    GpuAvailability,
    SubscribersToUrl,
    Subscribers,
    Urls,
    DBSession,
)
import yaml

app = FastAPI()

with open("config.yml", "r") as yml:
    cfg = yaml.safe_load(yml)


@app.get("/GetAvailableGPU")
def availableGPUs():
    with DBSession() as db:
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
    with DBSession() as db:
        subsToUrls = (
            db.query(
                Subscribers.name,
                Subscribers.email,
                Urls.url,
                Urls.short_name,
                Urls.comment,
                SubscribersToUrl.pattern,
            )
            .join(Subscribers)
            .join(Urls)
            .all()
        )
    return {"Subscribers": subsToUrls}


@app.get("/GetUrls")
def getUrls():
    with DBSession() as db:
        urls = db.query(
            Urls.url,
            Urls.short_name,
            Urls.comment,
        ).all()
    return {"available_urls": urls}
