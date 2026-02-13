import asyncio
import os
from playwright.async_api import async_playwright
from html import escape
from openpyxl import Workbook

INPUT_TXT = "domains3.txt"
SCREENSHOT_DIR = "screenshots"
OUTPUT_HTML = "report.html"
OUTPUT_XLSX = "results.xlsx"
CONCURRENCY = 4        # 3–5 is safe on Windows
TIMEOUT_MS = 15000

os.makedirs(SCREENSHOT_DIR, exist_ok=True)

HTML_HEADER = """<!doctype html>
<html>
<head>
  <meta charset="utf-8">
  <title>Domain Screenshot Report</title>
  <style>
    body { font-family: Arial, sans-serif; background: #0f1220; color: #e6e8ef; }
    .row { display: flex; gap: 16px; align-items: center; padding: 10px; border-bottom: 1px solid #2a2f55; }
    .domain { width: 320px; font-weight: 600; }
    .status { width: 90px; }
    .ok { color: #6ef3a5; }
    .err { color: #ff7b7b; }
    img { max-width: 420px; border-radius: 6px; box-shadow: 0 6px 16px rgba(0,0,0,.35); }
    .nosnap { opacity: .7; font-style: italic; }
  </style>
</head>
<body>
  <h1>Live Domain Screenshots</h1>
"""
HTML_FOOTER = "</body></html>\n"

async def capture(browser, sem, domain):
    async with sem:
        page = await browser.new_page(viewport={"width": 1280, "height": 800})
        filename = f"{domain.replace('.', '_')}.png"
        path = os.path.join(SCREENSHOT_DIR, filename)

        final_url = ""
        status = "ERROR"

        try:
            final_url = f"https://{domain}"
            await page.goto(final_url, timeout=TIMEOUT_MS, wait_until="networkidle")
            await page.screenshot(path=path, full_page=True)
            status = "OK"
        except Exception:
            try:
                final_url = f"http://{domain}"
                await page.goto(final_url, timeout=TIMEOUT_MS, wait_until="networkidle")
                await page.screenshot(path=path, full_page=True)
                status = "OK"
            except Exception:
                status = "ERROR"
                path = ""
        finally:
            await page.close()

        print(f"Snapshot: {domain} -> {status}")
        return domain, final_url, path, status

async def main():
    with open(INPUT_TXT, encoding="utf-8") as f:
        domains = [d.strip() for d in f if d.strip()]

    sem = asyncio.Semaphore(CONCURRENCY)

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        tasks = [capture(browser, sem, d) for d in domains]

        results = []
        for coro in asyncio.as_completed(tasks):
            results.append(await coro)

        await browser.close()

    # ---- Write HTML report ----
    with open(OUTPUT_HTML, "w", encoding="utf-8") as out:
        out.write(HTML_HEADER)
        for domain, final_url, path, status in results:
            out.write('<div class="row">')
            out.write(f'<div class="domain">{escape(domain)}</div>')
            out.write(f'<div class="status {"ok" if status=="OK" else "err"}">{status}</div>')
            if status == "OK" and path:
                out.write(f'<a href="{escape(final_url)}" target="_blank"><img src="{path}"></a>')
            else:
                out.write('<div class="nosnap">No screenshot</div>')
            out.write('</div>\n')
        out.write(HTML_FOOTER)

    # ---- Write Excel (.xlsx) ----
    wb = Workbook()
    ws = wb.active
    ws.title = "Results"
    ws.append(["Domain", "Final_URL", "Screenshot_Path", "Status"])

    for domain, final_url, path, status in results:
        ws.append([domain, final_url, path, status])

    wb.save(OUTPUT_XLSX)

    print(f"\nDone!")
    print(f"- Screenshots: ./{SCREENSHOT_DIR}")
    print(f"- HTML report: {OUTPUT_HTML}")
    print(f"- Excel file:  {OUTPUT_XLSX}")

if __name__ == "__main__":
    asyncio.run(main())
