import logging, asyncio, requests
from celery import shared_task
from django.conf import settings
from .utils import scraper_instance

logger = logging.getLogger(__name__)

async def scrape_data():
    await scraper_instance.scrape_resource_links()


@shared_task(bind=True, autoretry_for=(Exception,), retry_kwargs={'max_retries': 2, 'countdown': 5})
def trigger_scraper(self):
    asyncio.run(scrape_data())

@shared_task
def cron_scraper():
    req = requests.get(f"http://{settings.SCRAPER_URL}/api/scraper/run")
    if req.status_code == 200:
        logger.debug("[LOG] Scraper is triggered by cron.")