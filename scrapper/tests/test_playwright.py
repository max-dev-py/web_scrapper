from playwright.async_api import async_playwright
import asyncio


async def main():
    async with async_playwright() as p:
        browser = await p.chromium.connect("ws://127.0.0.1:3003/")
        page = await browser.new_page()
        await page.goto("https://example.com")
        print(await page.title())
        await browser.close()


asyncio.run(main())
