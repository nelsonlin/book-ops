
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path
import re

async def test_udn_extract():
    html_path = Path("output/investigation/udn.html").absolute()
    url = f"file://{html_path}"
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()
        await page.goto(url)
        
        platform_hint = 2
        
        # Test Date Extraction Logic
        date = None
        try:
            headings = page.locator("h3").filter(has_text="出版日期")
            count = await headings.count()
            print(f"Found {count} h3 headings with '出版日期'")
            for i in range(count):
                h = headings.nth(i)
                h_text = await h.inner_text()
                p_loc = h.locator("xpath=following-sibling::p")
                p_count = await p_loc.count()
                print(f"Heading {i}: '{h_text}', following p count: {p_count}")
                if p_count > 0:
                    text = await p_loc.first.inner_text()
                    print(f"  p text: '{text}'")
                    if text and "202" in text:
                        date = text
                        print(f"  -> Match found: {date}")
                        break
        except Exception as e:
            print(f"Error: {e}")
            
        print(f"Final extracted date: {date}")
        await browser.close()

if __name__ == "__main__":
    asyncio.run(test_udn_extract())
