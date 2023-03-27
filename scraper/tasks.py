import asyncio
import logging, aiohttp, asyncio
from celery import shared_task
from safari.models import Safari
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class ScraperBot:
    def __init__(self) -> None:
        "Initializing globally used variables."
        self.result = { "safari_data" : [] }
        self.headers = { 'User-Agent': 'Mozilla/5.0 (Linux; Android 11; RMX2101 Build/RKQ1.201217.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/108.0.5359.128 Mobile Safari/537.36 Line/12.21.1/IAB' }
        self.base_url_home = "https://www.safaribookings.com/tours/page/"
        self.base_url_detail = "https://www.safaribookings.com/tours/t"

    async def scrape_resource_links(self):
        async with aiohttp.ClientSession() as session:
            for counter in range(1, 3):
                async with session.get(f"{self.base_url_home}{counter}") as response:
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    # get tours by li
                    tours = soup.find_all('li', attrs={'class': 'col-t-6'})

                    for tour in tours:
                        url = tour.find('a', class_="list__item")['href']
                        logger.debug(url, "<-- There is a url!")
                        break
                
                break

async def scrape_data():
    safaris = ScraperBot()
    await safaris.scrape_resource_links()

@shared_task
def trigger_scraper():
    asyncio.run(scrape_data())