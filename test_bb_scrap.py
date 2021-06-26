import asyncio
from pyppeteer import launch
from bs4 import BeautifulSoup
from time import time

async def main():
    browser = await launch()
    page = await browser.newPage()
    page.setDefaultNavigationTimeout(0)
    start_time = time()
    url = "https://www.bestbuy.com/site/searchpage.jsp?st=gpu+cards"
    await page.goto(url,{"waitUntil": "domcontentloaded"})
    end_time = time()
    elapsed_time = end_time - start_time
    content = await page.content()
    await browser.close()

    soup = BeautifulSoup(content, 'html.parser')
    print(soup.title)
    print(f"url:{url} elapsed time: {elapsed_time}")

asyncio.get_event_loop().run_until_complete(main())