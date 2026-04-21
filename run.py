from bs4 import BeautifulSoup
#from playwright.sync_api import sync_playwright
import json
import requests

imo = 9648714
url = f"https://www.vesselfinder.com/vessels/details/{imo}"
headers = {"User-Agent": "Mozilla/5.0"}
html = requests.get(url, headers=headers).text
soup = BeautifulSoup(html, "lxml")

sections = [
        "History",
        f"Offshore Support Vessel, IMO {imo}",
        "Vessel Particulars",
        "Voyage Data"
]

master_dict = {}
# static data
for div in soup.find_all(["div", "section"]):
    heading = div.find("h2")
    if (heading is not None):
        head = heading.get_text(strip=True)
        if head in sections:
            print(heading.get_text(strip=True))
            rows = div.find_all("tr")
            rows = {row.find("td", class_="tpc1").get_text(strip=True):
                    row.find("td", class_="tpc2").get_text(strip=True)
                    for row in rows
                    if row.find("td", class_="tpc1")
                        and row.find("td", class_="tpc2")}
            rows = {k: v for k, v in rows.items() if (v != "") & (v != "-")}
            master_dict |= rows
# dynamic data
djson = json.loads(soup.find("div", attrs={"data-json": True})["data-json"])
keymap = {
        "Position received": "lrpd",
        "Latitude": "ship_lat",
        "Longitude": "ship_lon",
        "Course": "ship_cog",
        "Speed": "ship_sog"
}
newdjson = {newkey: djson[oldkey] for newkey, oldkey in keymap.items()}
master_dict |= newdjson
print(master_dict)
