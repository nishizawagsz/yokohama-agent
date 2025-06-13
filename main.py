from playwright.sync_api import sync_playwright
import pandas as pd
import datetime

# scraper URL-ek (most még csak homes.co.jp)
urls = [
    "https://www.homes.co.jp/chintai/kanagawa/list/?cond%5Broseneki%5D%5B60408950%5D=60408950&cond%5Broseneki%5D%5B60408951%5D=60408951&cond%5Bmonthmoneyroomh%5D=0&cond%5Bhousearea%5D=80&cond%5Bhouseageh%5D=0&cond%5Bwalkminutesh%5D=0&bukken_attr%5Bcategory%5D=chintai&bukken_attr%5Bpref%5D=14"
]

def fetch_listings(url):
    listings = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(url)
        page.wait_for_timeout(5000)

        items = page.query_selector_all("div.mod-bukkenList div.moduleInner")

        for item in items:
            title_el = item.query_selector(".bukkenSpec .bukkenName a")
            price_el = item.query_selector(".bukkenSpec .price .num")
            address_el = item.query_selector(".bukkenSpec .address")
            link_el = item.query_selector(".bukkenSpec .bukkenName a")

            title = title_el.inner_text().strip() if title_el else "Nincs cím"
            price = price_el.inner_text().strip() if price_el else "Nincs ár"
            address = address_el.inner_text().strip() if address_el else "Nincs címadat"
            link = link_el.get_attribute("href") if link_el else "#"

            if not link.startswith("http"):
                link = f"https://www.homes.co.jp{link}"

            listings.append({
                "title": title,
                "price": price,
                "address": address,
                "link": link
            })

        browser.close()
    return listings



def save_to_csv(all_listings):
    if all_listings:
        df = pd.DataFrame(all_listings)
        now = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M")
        filename = f"listings_{now}.csv"
        df.to_csv(filename, index=False)
        print(f"✅ CSV fájl mentve: {filename}")
    else:
        print("⚠️ Nincs találat a scraper által.")

def main():
    all_listings = []
    for url in urls:
        print(f"Oldal ellenőrzése: {url}")
        listings = fetch_listings(url)
        all_listings.extend(listings)

    save_to_csv(all_listings)

if __name__ == "__main__":
    main()
