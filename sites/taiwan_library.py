import asyncio
import json
import re
import os
from pathlib import Path
from urllib.parse import urljoin

from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)

from models import BookResult

BASE_URL = "https://taiwanlibrarysearch.herokuapp.com/"
DEBUG_DIR = Path("output") / "taiwan_library"

# Platform IDs for auto-fill logic
PLATFORM_IDS = {
    "HyRead": 1,
    "UDN": 2,
    "國立公共資訊圖書館": 3,
    "NTL": 3,
    "台灣雲端書庫": 4,
}

SEARCH_BOX_SELECTORS = [
    ("role:textbox", None),
    ("css", "input[type='search']"),
    ("css", "input[type='text']"),
    ("css", "input[name*='search']"),
    ("css", "input[id*='search']"),
    ("css", "input[name*='query']"),
    ("css", "input[id*='query']"),
]

SEARCH_BUTTON_SELECTORS = [
    ("role:button", "搜尋"),
    ("role:button", "Search"),
    ("role:button", "查詢"),
    ("css", "button[type='submit']"),
    ("css", "input[type='submit']"),
    ("css", "button"),
]

RESULT_ROW_SELECTORS = [
    ".items-body-content a",
    "div.content-block a",
]

NO_RESULT_PATTERNS = [
    r"沒有結果",
    r"查無資料",
    r"找不到",
]

HEADLESS_DEFAULT = os.getenv("CI", "false").lower() == "true"
TIMEOUT_MS = 30000


def search(book_name: str):
    return asyncio.run(_search_async(book_name))


async def _search_async(book_name: str):
    DEBUG_DIR.mkdir(parents=True, exist_ok=True)
    debug_log = []

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=HEADLESS_DEFAULT)
        context = await browser.new_context()
        page = await context.new_page()

        try:
            await _log(debug_log, f"goto {BASE_URL}")
            await page.goto(BASE_URL, wait_until="domcontentloaded", timeout=TIMEOUT_MS)
            await _dump_debug(page, "01_loaded", debug_log)

            search_box = await _find_search_box(page, debug_log)
            await search_box.fill(book_name)
            await _submit_search(page, search_box, debug_log)
            await _wait_for_search_state(page, debug_log)
            await _dump_debug(page, "02_after_search", debug_log)

            if await _looks_like_no_result(page):
                return []

            row_locator, selector_used = await _find_result_rows(page, debug_log)
            if row_locator is None:
                return []

            results = await _extract_results_from_rows(page, row_locator, selector_used, debug_log, context)
            results = _dedupe_results(results)
            await _write_debug_log(debug_log)
            return results

        except Exception as exc:
            await _log(debug_log, f"fatal error: {exc}")
            await _write_debug_log(debug_log)
            raise
        finally:
            await browser.close()


async def _find_search_box(page, debug_log):
    for kind, value in SEARCH_BOX_SELECTORS:
        try:
            locator = _build_locator(page, kind, value)
            await locator.first.wait_for(state="visible", timeout=2000)
            return locator.first
        except Exception: continue
    raise RuntimeError("Search box not found")


def _build_locator(page, kind, value):
    if kind == "role:textbox": return page.get_by_role("textbox")
    if kind == "role:button": return page.get_by_role("button", name=value)
    if kind == "css": return page.locator(value)
    raise ValueError(f"Unsupported locator kind: {kind}")


async def _submit_search(page, search_box, debug_log):
    for kind, value in SEARCH_BUTTON_SELECTORS:
        try:
            locator = _build_locator(page, kind, value)
            await locator.first.click()
            return
        except Exception: continue
    await search_box.press("Enter")


async def _wait_for_search_state(page, debug_log):
    try:
        await page.wait_for_load_state("networkidle", timeout=8000)
    except Exception: pass
    for selector in RESULT_ROW_SELECTORS:
        try:
            await page.locator(selector).first.wait_for(state="visible", timeout=2000)
            return
        except Exception: continue


async def _find_result_rows(page, debug_log):
    for selector in RESULT_ROW_SELECTORS:
        try:
            locator = page.locator(selector)
            if await locator.count() > 0:
                return locator, selector
        except Exception: continue
    return None, None


async def _extract_results_from_rows(page, rows, selector_used, debug_log, context=None):
    platforms = page.locator(".content-block")
    if await platforms.count() > 0:
        return await _extract_hierarchical(page, platforms, 20, debug_log, context)
    return []


async def _extract_hierarchical(page, platforms, limit, debug_log, context):
    results = []
    platform_count = await platforms.count()
    tasks_to_run = []
    
    for p_idx in range(min(platform_count, limit)):
        platform_el = platforms.nth(p_idx)
        platform_name = "Unknown"
        try:
            head = platform_el.locator(".items-head p")
            if await head.count() > 0: platform_name = _clean_text(await head.inner_text())
        except Exception: pass
        
        platform_id = _get_platform_id(platform_name)
        book_accordions = platform_el.locator(".accordion")
        book_count = await book_accordions.count()
        
        for b_idx in range(min(book_count, 20)):
            accordion = book_accordions.nth(b_idx)
            book_title = ""
            try:
                acc_title = accordion.locator(".accordion-title, .M-th")
                if await acc_title.count() > 0: book_title = _clean_text(await acc_title.inner_text())
            except Exception: pass
            
            library_links = accordion.locator("a[href]")
            for l_idx in range(min(await library_links.count(), 10)):
                link = library_links.nth(l_idx)
                try:
                    href = await link.get_attribute("href")
                    library_name = _clean_text(await link.inner_text())
                    if href and library_name:
                        tasks_to_run.append({
                            "pid": platform_id, "pname": platform_name,
                            "btitle": book_title, "lname": library_name, "url": urljoin(page.url, href)
                        })
                except Exception: continue

    if context and tasks_to_run:
        platform_firsts = {}
        for t in tasks_to_run:
            if t["pid"] not in platform_firsts: platform_firsts[t["pid"]] = t
        
        parallel_tasks = [
            _deep_crawl_for_metadata(t["url"], context, debug_log, t["pid"])
            for t in platform_firsts.values()
        ]
        metadatas = await asyncio.gather(*parallel_tasks, return_exceptions=True)
        platform_metas = {pid: (m if not isinstance(m, Exception) else {}) for pid, m in zip(platform_firsts.keys(), metadatas)}
    else: platform_metas = {}

    for t in tasks_to_run:
        meta = platform_metas.get(t["pid"], {})
        # Title logic fix
        final_title = meta.get("title") or t["btitle"]
        if t["pid"] == 3 and meta.get("title"):
            if any(g in meta["title"] for g in ["評論", "AI之眼", "AI世代", "Python"]):
                if len(t["btitle"]) > len(meta["title"]): final_title = t["btitle"]

        results.append(BookResult(
            title=final_title or "Unknown",
            author=meta.get("author") or "Unknown",
            format=meta.get("format") or "Unknown",
            date=_normalize_date(meta.get("date")),
            url=t["url"],
            source=f"{'國立公共資訊圖書館' if t['pid']==3 else t['pname']}/{t['lname']}",
            frontcover=meta.get("frontcover") or ""
        ))
    return results


async def _deep_crawl_for_metadata(url, context, debug_log, platform_hint=None):
    page = await context.new_page()
    metadata = {}
    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=TIMEOUT_MS)
        if platform_hint == 3:
            try:
                await page.wait_for_selector("#bookdetailcpcontentblock", timeout=10000)
                await asyncio.sleep(3)
            except Exception: pass
        elif platform_hint == 4:
            try: await page.wait_for_selector(".detail h2", timeout=10000)
            except Exception: pass

        for field in ["title", "author", "date", "format", "frontcover"]:
            metadata[field] = await _extract_detail_field(page, field, platform_hint)
    except Exception: pass
    finally: await page.close()
    return metadata


async def _extract_detail_field(page, field_type, platform_hint=None):
    try:
        if field_type == "title":
            if platform_hint == 1:
                el = page.locator("#center h3, .book-detail h3").first
                if await el.count() > 0: return _clean_text(await el.inner_text())
            if platform_hint == 3:
                el = page.locator(".cp_content h1, table.cptb h1").first
                if await el.count() > 0: return _clean_text(await el.inner_text())
            if platform_hint == 4:
                el = page.locator(".detail h2, h2").first
                if await el.count() > 0:
                    t = await el.inner_text()
                    if "雲端書庫" not in t: return _clean_text(t)
            
            selectors = ["h1", ".book-title", "meta[property='og:title']"]
            for s in selectors:
                try:
                    if s.startswith("meta"):
                        val = await page.locator(s).get_attribute("content")
                        if val: return _clean_text(val)
                    else:
                        el = page.locator(s).first
                        if await el.count() > 0: return _clean_text(await el.inner_text())
                except Exception: continue

        elif field_type == "author":
            if platform_hint == 1:
                el = page.locator("#center p:nth-child(4), p.note:has-text('作者')").first
                if await el.count() > 0: return _clean_metadata(await el.inner_text())
            if platform_hint == 3:
                el = page.locator("#bookdetailcpcontentblock li:has-text('作者') a, #bookdetailcpcontentblock li:has-text('作者')").first
                if await el.count() > 0: return _clean_metadata(await el.inner_text())
            if platform_hint == 4:
                el = page.locator("td:has-text('作者') + td, .detail-info li:has-text('作者')").first
                if await el.count() > 0: return _clean_metadata(await el.inner_text())
            
            body = await page.inner_text("body")
            m = re.search(r"作者[:：\s]*([^\n|｜\s]+)", body)
            if m: return _clean_metadata(m.group(1))

        elif field_type == "date":
            if platform_hint == 3:
                try:
                    labels = page.locator("#bookdetailcpcontentblock li").filter(has_text=re.compile(r"出版年|日期"))
                    for i in range(await labels.count()):
                        t = await labels.nth(i).inner_text()
                        m = re.search(r"(19|20)\d{2}", t)
                        if m and m.group(0) != "2025": return m.group(0)
                        m2 = re.search(r"民\s*(\d+)", t)
                        if m2: return str(1911 + int(m2.group(1)))
                except Exception: pass
            elif platform_hint == 2:
                try:
                    el = page.locator("h3:has-text('出版日期') + p").first
                    if await el.count() > 0: return await el.inner_text()
                except Exception: pass
            
            body = await page.inner_text("body")
            m = re.search(r"出版日期[:：\s]*(?!線上)(19|20)\d{2}[/-]\d{1,2}[/-]\d{1,2}", body)
            if m: return m.group(0)

        elif field_type == "format":
            if platform_hint == 4: return "N/A"
            body = (await page.inner_text("body")).upper()
            if "EPUB" in body: return "EPUB"
            if "PDF" in body: return "PDF"

        elif field_type == "frontcover":
            selectors = [".book-cover img", "#bookdetailcpcontentblock figure img", ".cover img", "img[alt='cover']"]
            for s in selectors:
                try:
                    el = page.locator(s).first
                    if await el.count() > 0:
                        src = await el.get_attribute("src") or await el.get_attribute("data-original")
                        if src and src.startswith("http") and "thumb" not in src.lower(): return src
                except Exception: continue
    except Exception: pass
    return None


def _get_platform_id(name):
    name = name.lower()
    for k, v in PLATFORM_IDS.items():
        if k.lower() in name: return v
    return 0


async def _looks_like_no_result(page):
    try:
        body_text = (await page.locator("body").inner_text()).lower()
        for pattern in NO_RESULT_PATTERNS:
            if re.search(pattern, body_text, re.IGNORECASE): return True
    except Exception: pass
    return False


def _looks_like_bookish_row(title, text):
    blob = f"{title} {text}".strip().lower()
    if len(blob) < 2: return False
    blocked_terms = ["首頁", "home", "登入", "login", "註冊", "register", "search"]
    return not any(term in blob for term in blocked_terms)


def _normalize_date(d):
    if not d: return ""
    # Try full date (YYYY-MM-DD or YYYY/MM/DD)
    m = re.search(r"((?:19|20)\d{2})([-/.])(1[0-2]|0?[1-9])\2([12][0-9]|3[01]|0?[1-9])", d)
    if m:
        return f"{m.group(1)}-{int(m.group(3)):02d}-{int(m.group(4)):02d}"
    # Try year only
    m = re.search(r"(19|20)\d{2}", d)
    if m:
        return f"{m.group(0)}-01-01"
    return ""


def _clean_text(t):
    return re.sub(r"\s+", " ", t).strip() if t else ""


def _clean_metadata(t, f=None):
    if not t: return ""
    t = re.sub(r"^(作者|出版年|格式|日期)[:：\s]*", "", t).strip()
    return re.sub(r"(著|編|譯)$", "", t).strip()


def _dedupe_results(res):
    seen = set()
    deduped = []
    for r in res:
        key = (r.title.lower(), r.url.lower())
        if key not in seen:
            seen.add(key)
            deduped.append(r)
    return deduped


async def _log(log, msg):
    line = f"[taiwan_library] {msg}"
    print(line)
    log.append(line)


async def _dump_debug(page, tag, log):
    try:
        await page.screenshot(path=str(DEBUG_DIR / f"{tag}.png"))
        (DEBUG_DIR / f"{tag}.html").write_text(await page.content(), encoding="utf-8")
    except Exception: pass


async def _write_debug_log(log):
    (DEBUG_DIR / "debug.log").write_text("\n".join(log), encoding="utf-8")
