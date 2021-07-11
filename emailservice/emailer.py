from db import (
    GpuAvailability,
    SubscribersToUrl,
    Subscribers,
    Urls,
    DBSession,
)
import re
import smtplib
from email.message import EmailMessage
import yaml

with open("config.yml", "r") as yml:
    cfg = yaml.safe_load(yml)


def check_db_for_patterns():
    with DBSession() as db:
        subscribers = (
            db.query(
                Subscribers,
                Urls,
                SubscribersToUrl,
            )
            .join(Subscribers)
            .join(Urls)
            .all()
        )
        gpus = (
            db.query(
                GpuAvailability,
            )
            .filter(GpuAvailability.available == True)
            .all()
        )
        match_list = []
        for sub in subscribers:
            p = sub.SubscribersToUrl.pattern
            gpus_matched = search_pattern_in_gpus(p, gpus)
            if len(gpus_matched) > 0:
                match_list.append(
                    {"email": sub.Subscribers.email, "gpus": gpus_matched}
                )
    return match_list


def search_pattern_in_gpus(pattern: str, gpus: list[GpuAvailability]):
    return [item for item in gpus if re.search(pattern, item.name)]


def send_email(match_list: list[dict]):
    port = cfg["emailer"]["port"]
    smtpserver = cfg["emailer"]["server"]
    sender = cfg["emailer"]["username"]
    password = cfg["emailer"]["password"]
    for m in match_list:
        receiver = m["email"]
        message, subject = generate_message(m["gpus"])
        try:
            msg = EmailMessage()
            msg["From"] = sender
            msg["To"] = receiver
            msg["Subject"] = subject
            msg.set_content(message)
            with smtplib.SMTP_SSL(smtpserver, port) as server:
                server.login(sender, password)
                server.send_message(msg)
        except Exception as e:
            print(f"Failed to send email with error: {e}")


def generate_message(gpus: list[GpuAvailability]):
    gpus_info = []
    for gpu in gpus:
        gpu_str = "\n".join(
            [
                "name: " + gpu.name,
                "model: " + gpu.model,
                "sku: " + gpu.sku,
                "price: " + str(gpu.price),
                "update_time: " + gpu.update_time.strftime("%Y%m%d %H:%M:%S"),
            ]
        )
        gpu_str = gpu_str + "\n"
        gpus_info.append(gpu_str)
    subject = "GPU Available"
    gpu_info_str = "\n".join(gpus_info)
    message = f"\nHello,\nGood News! the following gpus are available:\n{gpu_info_str}"
    return message, subject


def run_email_service():
    print("running email service..")
    match_list = check_db_for_patterns()
    if len(match_list) > 0:
        send_email(match_list)
    print("email service finished!")


if __name__ == "__main__":
    check_db_for_patterns()
