import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import csv

ua = UserAgent()
headers = {'User-Agent': ua.random}

def get_listings(url):
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    results = []

    listings = soup.find_all('div', class_='result')
    for listing in listings:
        name = listing.find('a', class_='business-name')
        phone = listing.find('div', class_='phones')
        address = listing.find('div', class_='street-address')
        category = listing.find('div', class_='categories')

        results.append({
            'Name': name.text.strip() if name else '',
            'Phone': phone.text.strip() if phone else '',
            'Address': address.text.strip() if address else '',
            'Category': category.text.strip() if category else '',
        })

    return results

url = "https://www.yellowpages.com/search?search_terms=plumber&geo_location_terms=Miami%2C+FL"
data = get_listings(url)

with open('yellowpages_output.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['Name', 'Phone', 'Address', 'Category'])
    writer.writeheader()
    writer.writerows(data)

print("Scraping complete!")
