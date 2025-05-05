from fastapi import FastAPI, Query
import os
from playwright.async_api import async_playwright
import asyncio

app = FastAPI()


@app.get("/")
async def test_playwright():
    # Получаем URL WebSocket сервера из переменной окружения
    playwright_ws_url = os.getenv("PLAYWRIGHT_WS_URL", "ws://localhost:3000")

    async with async_playwright() as p:
        # Подключаемся к Playwright серверу
        browser = await p.chromium.connect(playwright_ws_url)
        page = await browser.new_page()
        await page.goto("https://example.com")
        title = await page.title()
        await browser.close()

    return {"title": title}

@app.get("/scrape")
async def scrape(symbol: str = Query(..., description="TICKER")):
    """
    Scrape a webpage based on the given query parameter.

    Args:
        query (str): Параметр, добавляемый к URL для скрэпинга.

    Returns:
        dict: Скрэйпнутые данные в виде JSON.
    """
    # Формируем URL на основе параметра
    target_url = f"https://www.tradingview.com/chart/?symbol={symbol}"
    # print(target_url)

    playwright_ws_url = os.getenv("PLAYWRIGHT_WS_URL", "ws://localhost:3000")

    async with async_playwright() as p:
        # Подключаемся к Playwright серверу
        browser = await p.chromium.connect(playwright_ws_url)

        page = await browser.new_page()
        await page.set_extra_http_headers({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        })

        await page.goto(target_url, timeout=30000, wait_until="domcontentloaded")
        title = await page.title()
        content = await page.content()

        try:
            price_element = page.locator('.price-qWcO4bp9')
            price = await price_element.inner_text()
            status = "success"
        except Exception as e:
            return {
                'status': 'error',
                'message': str(e),
                "title": title,
                # 'page_source': content,
            }

        await browser.close()

    return {
        'status': status,
        "title": title,
        "url": target_url,
        "price": price,
        # 'page_source': content,
    }