from typing import List
from fastapi import FastAPI
from db import (
    GpuAvailability,
    SubscribersToUrl,
    Subscribers,
    Urls,
    DBSession,
)
from pydantic import BaseModel
from datetime import datetime

app = FastAPI()


class PostResponseStatus(BaseModel):
    status: str
    err_msg: str


class ResponseAvailableGPUItem(BaseModel):
    name: str
    model: str
    sku: str
    available: bool
    price: float
    update_time: datetime


class ResponseAvailableGPU(BaseModel):
    available_list: List[ResponseAvailableGPUItem]


@app.get("/GetAvailableGPU", response_model=ResponseAvailableGPU)
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
    ret = ResponseAvailableGPU(available_list=[])
    for gpu in available_gpus:
        gpu_item = ResponseAvailableGPUItem(
            name=gpu.name,
            model=gpu.model,
            sku=gpu.sku,
            available=gpu.available,
            price=gpu.price,
            update_time=gpu.update_time,
        )
        ret.available_list.append(gpu_item)
    return ret


class Subscriber(BaseModel):
    name: str
    email: str


@app.post("/AddSubscriber", response_model=PostResponseStatus)
async def addSubscriber(sub: Subscriber):
    new_sub = Subscribers(name=sub.name, email=sub.email)
    try:
        with DBSession() as db:
            db.add(new_sub)
            db.commit()
            ret = PostResponseStatus(status="success", err_msg="")
    except Exception as e:
        err_msg = f"failed to add new subscriber, error: {e}"
        ret = PostResponseStatus(status="error", err_msg=err_msg)
    return ret


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
