import asyncio
import httpx
import csv
import ssl

INPUT_FILE = "domains2.txt"
OUTPUT_FILE = "domain_access_results.csv"
CONCURRENCY = 40  # safer for Windows + home networks

def classify(status):
    if status == 200:
        return "LIVE"
    if status in [301, 302, 307, 308]:
        return "LIVE (REDIRECT)"
    if status == 403:
        return "BLOCKED"
    if status in [404, 410]:
        return "NOT FOUND"
    if isinstance(status, int) and 500 <= status < 600:
        return "SERVER ERROR"
    if status == "SSL ERROR":
        return "SSL ERROR"
    if status == "ERROR":
        return "OFFLINE / DNS / TIMEOUT"
    return "UNKNOWN"

async def check_domain(client, domain):
    urls = [f"https://{domain}", f"http://{domain}"]
    for url in urls:
        try:
            r = await client.get(url)
            return domain, r.status_code, classify(r.status_code), str(r.url)
        except (httpx.RequestError, ssl.SSLError):
            continue
        except Exception:
            continue
    return domain, "ERROR", classify("ERROR"), ""

async def main():
    with open(INPUT_FILE) as f:
        domains = [d.strip() for d in f if d.strip()]

    sem = asyncio.Semaphore(CONCURRENCY)

    limits = httpx.Limits(max_connections=CONCURRENCY)
    timeout = httpx.Timeout(10.0)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
    }

    async with httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        headers=headers,
        follow_redirects=True,
        verify=False  # <--- important: ignore broken TLS
    ) as client:

        async def bounded_check(domain):
            async with sem:
                return await check_domain(client, domain)

        tasks = [bounded_check(d) for d in domains]
        results = await asyncio.gather(*tasks, return_exceptions=False)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["Domain", "HTTP_Status", "Classification", "Final_URL"])
        writer.writerows(results)

    print(f"\nDone! Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    asyncio.run(main())
