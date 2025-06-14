from playwright.sync_api import sync_playwright
import pandas as pd
import datetime
import http.server
import socketserver
import threading
import time

URL = "https://www.homes.co.jp/chintai/kanagawa/list/?cond%5Broseneki%5D%5B60408950%5D=60408950&cond%5Broseneki%5D%5B60408951%5D=60408951&cond%5Bmonthmoneyroomh%5D=0&cond%5Bhousearea%5D=80&cond%5Bhouseageh%5D=0&cond%5Bwalkminutesh%5D=0&bukken_attr%5Bcategory%5D=chintai&bukken_attr%5Bpref%5D=14"

def fetch_listings(url):
    listings = []
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Emberi user-agent!
        page = browser.new_page(user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
        print("Oldal betöltése: ", url)
        page.goto(url)
        page.wait_for_timeout(8000)  # várunk 8 másodpercet

        # Lementjük a teljes HTML-t
        html = page.content()
        with open("page_debug.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("DEBUG: HTML page saved.")

        # Megpróbáljuk lekérni a találatokat (ha van)
        items = page.query_selector_all(".mod-bukkenList .moduleInner")
        print(f"Talált {len(items)} találatot az oldalon!")

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

def serve_debug_file():
    PORT = 10000
    Handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"Serving at port {PORT}")
        httpd.serve_forever()

def main():
    fetch_listings(URL)
    # Szükség esetén ide teheted a save_to_csv-t is, ha listákat akarunk menteni

if __name__ == "__main__":
    main()
    # Elindítjuk a webszervert külön szálon, hogy elérd a fájlt böngészőből
    threading.Thread(target=serve_debug_file, daemon=True).start()
    print("A szerver 10 percig elérhető lesz a page_debug.html letöltéséhez!")
    time.sleep(600)  # 10 percig vár, hogy legyen időd letölteni
