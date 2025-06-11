from playwright.sync_api import sync_playwright
import pandas as pd
import datetime

def fetch_listings():
    url = "https://www.rentersnet.jp/search/area?city=14118&layout=4LDK"
    listings = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        items = page.query_selector_all("div.itemList li.item")
        
        for item in items:
            title = item.query_selector("div.itemTitle a").inner_text().strip()
            details = item.query_selector("div.itemData").inner_text().strip()
            link = item.query_selector("div.itemTitle a").get_attribute("href")

            listings.append({
                "title": title,
                "details": details,
                "link": f"https://www.rentersnet.jp{link}"
            })

        browser.close()

    return listings

def save_to_csv(listings):
    if listings:
        df = pd.DataFrame(listings)
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"listings_{now}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ CSV fájl mentve: {filename}")
    else:
        print("⚠️ Nincs találat a scraper által.")

def main():
    listings = fetch_listings()
    save_to_csv(listings)

if __name__ == "__main__":
    main()
