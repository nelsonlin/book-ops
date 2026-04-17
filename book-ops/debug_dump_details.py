
import asyncio
from playwright.async_api import async_playwright
from pathlib import Path

async def dump_detail_pages():
    output_dir = Path("output/investigation")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    urls = {
        "udn": "https://reading.udn.com/udnlib/tpml/B/178751",
        "ntl": "https://ebook.nlpi.edu.tw/bookdetail/58333",
        "cloud": "https://www.ebookservice.tw/ntl2/book/9464859e-1175-4339-8e8c-839c00e4f72e"
    }
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        
        for name, url in urls.items():
            print(f"Dumping {name}: {url}")
            page = await context.new_page()
            try:
                await page.goto(url, wait_until="networkidle", timeout=60000)
                html = await page.content()
                (output_dir / f"{name}.html").write_text(html, encoding="utf-8")
                await page.screenshot(path=str(output_dir / f"{name}.png"))
                print(f"  Done {name}")
            except Exception as e:
                print(f"  Failed {name}: {e}")
            finally:
                await page.close()
        
        await browser.close()

if __name__ == "__main__":
    asyncio.run(dump_detail_pages())
