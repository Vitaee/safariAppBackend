import asyncio
import logging, aiohttp, asyncio
from celery import shared_task

logger = logging.getLogger(__name__)


async def scrape_data():
    async with aiohttp.ClientSession() as session:
        async with session.get('https://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html') as response:
            html = await response.text()
            logger.debug('Hey man its works!')
            return { 'data' : html }

@shared_task
def trigger_scraper():
    asyncio.run(scrape_data())