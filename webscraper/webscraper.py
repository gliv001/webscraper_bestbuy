import os
from decimal import Decimal
from re import sub
from webscraper.gpu import GPU
from db import GpuAvailability, DBSession
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import time
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, wait
import yaml


def writeGPUToCSV(filepath, gpu_list: list[GPU]):
    with open(filepath, "a+") as f:
        for gpu in gpu_list:
            f.write(f"{gpu.getStringCSV()}\n")


def convertCurrencyToDecimal(money: str) -> float:
    return float(Decimal(sub(r"[^\d.]", "", money)))


def writeGPUToDB(gpu_list: list[GPU]):
    db_gpu_buffer = []
    for gpu in gpu_list:
        price = convertCurrencyToDecimal(gpu.price)
        db_gpu = GpuAvailability(
            name=gpu.name,
            model=gpu.model,
            sku=gpu.sku,
            available=gpu.available,
            price=price,
            update_time=datetime.now(),
        )
        db_gpu_buffer.append(db_gpu)
    try:
        with DBSession() as db:
            db.add_all(db_gpu_buffer)
            db.commit()
    except Exception as e:
        print(f"failed to update gpu list to db, error: {e}")


def getPageList(html):
    page_list = []
    footer = html.find("div", {"class": "footer top-border wrapper"})
    right_div = footer.find("div", {"class": "right-side"})
    ol = right_div.div.findAll("div")[1].ol
    for li in ol.findAll("li"):
        if li.a:
            page = {"page_number": int(li.a.text.strip()), "link": li.a["href"]}
            page_list.append(page)
    return page_list


def getLastPage(page_list):
    last_page = 1
    for page in page_list:
        if page["page_number"] > last_page:
            last_page = page["page_number"]
    return last_page


def load_page(page_url):
    start = time()
    driver = create_driver()
    driver.get(page_url)
    end = time()
    print(f"url:{page_url} elapsed time:{end-start}")
    page_html = driver.page_source
    driver.close()
    return page_html


def scrapePageNumbers(page_url):
    page_html = load_page(page_url)
    soup = BeautifulSoup(page_html, "html.parser")
    return getPageList(soup)


def scrapePage(page_url):
    page_html = load_page(page_url)
    soup = BeautifulSoup(page_html, "html.parser")

    div_main = soup.find("div", {"id": "main-results"})

    gpu_list = []
    for li in div_main.findAll("li", {"class": "sku-item"}):
        try:
            item_name = li.find("h4", {"class": "sku-header"}).a.text.strip()

            div = li.find("div", {"class": "sku-model"})
            div_model_sku = div.findAll("span", {"class": "sku-value"})
            if len(div_model_sku) >= 2:
                item_model = div_model_sku[0].text.strip()
                item_sku = div_model_sku[1].text.strip()
            else:
                item_model = ""
                item_sku = ""

            div = li.find(
                "div", {"class": "priceView-hero-price priceView-customer-price"}
            )
            item_price = div.span.text.strip().replace(",", "")

            div = li.find("div", {"class": "fulfillment-add-to-cart-button"})
            item_available = div.div.div.button.text.strip()
            if item_available.lower() == "sold out":
                available = False
            else:
                available = True

            gpu_list.append(GPU(item_name, item_model, item_sku, item_price, available))
        except Exception as e:
            # with open("config.yml", "r") as yml:
            #     cfg = yaml.safe_load(yml)
            # if not os.path.exists(cfg["output"]["logs_dir"]):
            #     os.makedirs(cfg["output"]["logs_dir"])
            # timestamp = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
            # filepath = os.path.join(
            #     cfg["output"]["logs_dir"], f"li_error_{timestamp}.html"
            # )
            # with open(filepath, "w") as f:
            #     f.write(li.text)
            # print(f"Error parsing line item, saved at [{filepath}], skipping.. {e}")
            print("Error parsing a line item")
    return gpu_list


def create_driver():
    options = Options()
    user_agent = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2"
    options.add_argument(f"user-agent={user_agent}")
    options.add_argument("--no-proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--headless")
    driver = Chrome(executable_path="./webscraper/chromedriver", options=options)
    return driver


def bestbuy_gpu_webscraper():
    print("starting webscraper..")
    with open("config.yml", "r") as yml:
        cfg = yaml.safe_load(yml)

    page_url = cfg["input"]["url"]
    # createGPUCSV("./output/output.csv")

    page_list = scrapePageNumbers(page_url)

    last_page = getLastPage(page_list)

    futures = []
    with ThreadPoolExecutor() as executor:
        futures.append(executor.submit(scrapePage, page_url))
        for n in range(2, last_page + 1):
            next_url = cfg["input"]["url_by_page"].format(n=n)
            futures.append(executor.submit(scrapePage, next_url))

    wait(futures)
    try:
        with DBSession() as db:
            db.execute("truncate table gpu_availability")
            db.commit()
    except Exception as e:
        print(f"failed to remove old gpu list from db, error: {e}")
    for future in futures:
        writeGPUToDB(future.result())
    print("webscraper finished!")


if __name__ == "__main__":
    start = time()
    bestbuy_gpu_webscraper()
    end = time()
    print(f"total elapsed time:{end-start}")
