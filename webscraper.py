from gpu import GPU
from bs4 import BeautifulSoup
from time import time
from pyppeteer import launch
import asyncio

def createGPUCSV(filepath):
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
    last_page_num = 1
    for page in page_list:
        if page["page_number"] > last_page_num:
            last_page_num = page["page_number"]
            last_page = page
    return last_page

async def scrapePage(page_url, create_html_file = False):
    browser = await launch()
    page = await browser.newPage()
    start_time = time()
    await page.goto(page_url,{"timeout": 0, "waitUntil": "domcontentloaded"})
    end_time = time()
    elapsed_time = end_time - start_time
    print(f"url:{page_url} elapsed time: {elapsed_time}")
    content = await page.content()
    await browser.close()

    soup = BeautifulSoup(content, "html.parser")

    if create_html_file == True:
        with open("output.html", "w") as f:
            f.write(soup.prettify())

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
            print(f"Error attempting to parse: {e}")
            pass # skip it if data can't be scraped
    return gpu_list, page_list

async def bestbuy_gpu_webscraper():
    page_url = "https://www.bestbuy.com/site/searchpage.jsp?st=gpu+cards"
    createGPUCSV("output.csv")

    gpu_list, page_list = await scrapePage(page_url, True)
    writeGPUToCSV("output.csv", gpu_list)
    last_page = getLastPage(page_list)
    
    futures = []
    for page_num in range(2, last_page["page_number"]+1):
        next_url = last_page["link"].replace(str(last_page["page_number"]), str(page_num))
        futures.append(asyncio.create_task(scrapePage(next_url)))

    results = await asyncio.gather(*futures)
    for result in results:
        gpu_list = result[0]
        writeGPUToCSV("output.csv", gpu_list)
    

if __name__ == "__main__":
    start = time()
    asyncio.get_event_loop().run_until_complete(bestbuy_gpu_webscraper())
    end = time()
    print(f"total elapsed time {end-start}")
    # while True:
    #     sleep(minutes*60)
    #     asyncio.get_event_loop().run_until_complete(bestbuy_gpu_webscraper())