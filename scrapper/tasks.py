from playwright.async_api import async_playwright
from celery import Celery

celery = Celery(__name__, broker="redis://redis:6379/0")


@celery.task(name="tasks.scrape_url")
def scrape_url(url):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        content = await page.content()
        await browser.close()
        return content