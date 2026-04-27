# -*- coding: utf-8 -*-
"""
/app/scraper.py
Module responsible for scraping ship data from various databases.
"""
import json
import requests

from bs4 import BeautifulSoup
import pandas as pd

from app.sources import Source

class Scraper:
    def __init__(self, source:Source):
        """
        Args:
            source (Source): A Source StrEnum value indicating the source from
            which to scrape the data.
        """
        self.source = source
        match source:
            case Source.VESSELFINDER:
                self.parse = self._parse_vesselfinder
            case _:
                print("A parser for requested source is not implemented.")

    def scrape(self, imo:str) -> pd.DataFrame:
        """
        One iteration of fetch sequence.

        Args:
            imo (str): A str containing the 7-digit IMO.

        Returns:
            DataFrame: DataFrame containing values extracted from the scraped data.
        """

        soup = self.get_web_contents(imo)
        return self.parse(soup)

    def get_web_contents(self, imo: str) -> BeautifulSoup:
        """
        Create a connection session to target source and fetches rendered web
        content.

        Args:
            imo (str): A str containing the 7-digit IMO.

        Returns:
            BeautifulSoup: A Soup instance containing the fetched web contents.
        """
        url = f"{self.source.value}{imo}"
        headers = {"User-Agent": "Mozilla/5.0"}
        html = requests.get(url, headers=headers).text
        soup = BeautifulSoup(html, "lxml")

        return soup

    def _parse_vesselfinder(self, soup: BeautifulSoup) -> pd.DataFrame:
        """
        Parser for fetching VesselFinder web contents.

        Args:
            soup (BeautifulSoup): A Soup instance containing the fetched web
            contents.

        Returns:
            DataFrame: A pandas DataFrame object containing desired values.
        """
        sections = [
                "History",
                f"Offshore Support Vessel, IMO {imo}",
                "Vessel Particulars",
                "Voyage Data"
        ]
        master_dict = {}
        # static data
        notinservice = soup.find("div", class_="notInService")
        if notinservice is not None:
            print(notinservice)
            print(notinservice.get_text(strip=True).split(' ')[-1])
        for div in soup.find_all(["div", "section"]):
            heading = div.find("h2")
            if (heading is not None):
                head = heading.get_text(strip=True)
                if head in sections:
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
        newdjson = {key: value for key, value in djson.items() if value != "-"}
        keymap = {
                "imo": "IMO number",
                "name": "Vessel Name",
                "ship_type": "Ship Type",
                "date_built": "Year of Build",
                "length_m": "Length Overall(m)",
                "beam_m": "Beam(m)",
                "gross_tonnage": "Gross Tonnage",
                "deadweight_t": "Deadweight(t)",
                "last_updated": "lrpd",
                "latitude": "ship_lat",
                "longitude": "ship_lon",
                "course": "ship_cog",
                "speed": "ship_sog"
        }
        master_dict |= djson
        master_dict = {newkey: master_dict[oldkey] for newkey, oldkey in keymap.items()}
        return pd.DataFrame([master_dict])

if __name__ == "__main__":
    imo = 9648714
    source = Source.VESSELFINDER
    scraper = Scraper(source)
    soup = scraper.get_web_contents(imo)
    dataframe = scraper.parse(soup)
    print(dataframe)
