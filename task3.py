import  requests
from lxml import html
from bs4 import BeautifulSoup
from pymongo import MongoClient
import time

# url = "https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page=1"
def scrape_page(url):
    response = requests.get(url, headers={"User-Agent":
                        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                        " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"})
    page = html.fromstring(response.content)
    rows = page.xpath("//table[@class='records-table']/tbody/tr")
    my_list = []
    for row in rows:
        every_row = row.xpath(".//td/text()")
        my_list.append({
            "Rank": every_row[0].strip(),
            "Mark": every_row[1].strip(),
            "Wind": every_row[2].strip(),
            "Competitor": row.xpath(".//td[4]/a/text()")[0].strip(),
            "DOB": every_row[5].strip(),
            "Nat": every_row[7].strip(),
            "Pos": every_row[8].strip(),
            "Venue": every_row[9].strip(),
            "Date": every_row[10].strip(),
            "ResultsScore": every_row[11].strip()
        })
    return my_list

def save_to_mongo(my_list):
    client = MongoClient("localhost", 27017)
    db = client["world_athletics"]
    collection = db["60_meaters_women"]
    collection.insert_many(my_list)

def main_function():
    main_url = "https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page="
    for number in range(1, 5):
        work_url = main_url + str(number)
        work_list = scrape_page(work_url)
        save_to_mongo(work_list)
        time.sleep(3)
        print("Next page: ", work_url)


if __name__ == "__main__":
    main_function()
    print("Finish BRO!)")


