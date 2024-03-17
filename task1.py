import  requests
from lxml import html
from bs4 import BeautifulSoup


url = "https://worldathletics.org/records/toplists/sprints/60-metres/indoor/women/senior/2023?page=1"

response = requests.get(url, headers={"User-Agent":
                    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)"
                    " AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15"})
page = html.fromstring(response.content)
rows = page.xpath("//table[@class='records-table']/tbody/tr")

first_row = rows[0].xpath(".//td/text()")
for el in first_row:
    print(el.encode('utf-8'))

