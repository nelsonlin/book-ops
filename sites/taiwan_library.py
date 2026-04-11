import asyncio
from pathlib import Path
from playwright.async_api import async_playwright, TimeoutError as PlaywrightTimeoutError
from models import BookResult

BASE_URL = "https://taiwanlibrarysearch.herokuapp.com/"
DEBUG_DIR = Path("output")

def search(book_name: str):
    return asyncio.run(_search_async(book_name))

async def _search_async(book_name: str):
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        try:
            await page.goto(BASE_URL, wait_until="domcontentloaded", timeout=30000)

            textbox = page.get_by_role("textbox")
            await textbox.fill(book_name)

            buttons = page.get_by_role("button")
            if await buttons.count() > 0:
                await buttons.first.click()
            else:
                await textbox.press("Enter")

            try:
                await page.wait_for_load_state("networkidle", timeout=10000)
            except PlaywrightTimeoutError:
                pass

            await page.screenshot(path=str(DEBUG_DIR / "taiwan_library.png"), full_page=True)

            return [BookResult(title=book_name, author="Unknown", format="Unknown", date="", url=page.url, source="taiwan_library")]

        except Exception:
            await page.screenshot(path=str(DEBUG_DIR / "taiwan_library_error.png"), full_page=True)
