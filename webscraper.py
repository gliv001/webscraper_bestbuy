import os
from gpu import GPU
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from time import time
from datetime import datetime

def createGPUCSV(filepath):
    if not os.path.exists(os.path.dirname(filepath)):
        os.makedirs(os.path.dirname(filepath))
    with open(filepath, 'w') as f:
        f.write(f"{GPU.getHeaderCSV()}\n")

def writeGPUToCSV(filepath, gpu_list):
    with open(filepath, 'a+') as f:
        for gpu in gpu_list:
            f.write(f"{gpu.getStringCSV()}\n")

def getPageList(html):
    page_list = []
    footer = html.find("div", {"class": "footer top-border wrapper"})
    right_div = footer.find("div", {"class": "right-side"})
    ol = right_div.div.findAll("div")[1].ol
    for li in ol.findAll('li'):
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

def scrapePage(driver, page_url):
    start = time()
    driver.get(page_url)
    end = time()
    print(f"url:{page_url} elapsed time:{end-start}")
    page_html = driver.page_source
    
    soup = BeautifulSoup(page_html, "html.parser")

    page_list = getPageList(soup)

    div_main = soup.find('div', {"id":"main-results"})
        
    gpu_list = []
    for li in div_main.findAll('li', {'class': 'sku-item'}):
        try:
            item_name = li.find('h4', {'class':'sku-header'}).a.text.strip()

            div = li.find('div', {'class':'sku-model'})
            div_model_sku = div.findAll('span', {'class':'sku-value'})
            if len(div_model_sku) >= 2:
                item_model = div_model_sku[0].text.strip()
                item_sku = div_model_sku[1].text.strip()
            else:
                item_model = ""
                item_sku = ""

            div = li.find('div', {'class':'priceView-hero-price priceView-customer-price'})
            item_price = div.span.text.strip().replace(',','')

            div = li.find('div', {'class':'fulfillment-add-to-cart-button'})
            item_available = div.div.div.button.text.strip()
            if item_available.lower() == "sold out":
                available = False
            else:
                available = True
            
            gpu_list.append(GPU(item_name, item_model, item_sku, item_price, available))
        except Exception as e:
            if not os.path.exists("./logs/errors"):
                os.makedirs("./logs/errors/")
            timestamp = datetime.strftime(datetime.now(), "%Y%m%d_%H%M%S")
            filepath = f"./logs/errors/li_error_{timestamp}.html"
            with open(filepath, "w") as f:
                f.write(li.text)
            print(f'Error parsing line item, saved at [{filepath}], skipping.. {e}')
    return gpu_list, page_list

def bestbuy_gpu_webscraper():
    page_url = "https://www.bestbuy.com/site/searchpage.jsp?st=gpu+cards"
    createGPUCSV("./output/output.csv")

    options = Options()
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    options.add_argument(f'user-agent={user_agent}')
    options.add_argument("--no-proxy-server='direct://'")
    options.add_argument("--proxy-bypass-list=*")
    options.add_argument("--headless")
    driver = Chrome(executable_path="./chromedriver", options=options)
    gpu_list, page_list = scrapePage(driver, page_url)
    writeGPUToCSV("./output/output.csv", gpu_list)
    last_page = getLastPage(page_list)
    for page_num in range(2, last_page+1):
        page = next((p for p in page_list if p["page_number"] == page_num), None)
        next_url = page["link"]
        gpu_list, page_list = scrapePage(driver, next_url)
        writeGPUToCSV("./output/output.csv", gpu_list)
    
    driver.close()

if __name__ == "__main__":
    start = time()
    bestbuy_gpu_webscraper()
    end = time()
    print(f"total elapsed time:{end-start}")