import requests
import csv
from bs4 import BeautifulSoup

source = requests.get('https://www.diac.ca/directory/?wpbdp_view=all_listings').text

soup = BeautifulSoup(source, 'lxml')

csv_file = open('scrape-test.csv', 'w')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['company', 'website'])

page = 1
while True:
    print('Page no. {}'.format(page))
    print('-' * 80)
    for i in soup.find_all('div', class_='wpbdp-listing'):
        company = i.find('div', class_='listing-title').a.text
        print(company)

        try:
            category = i.find('div', class_='wpbdp-field-association-category').span.a.text
            print(category)
        except Exception as e:
            category = 'none'

        try: 
            website = i.find('div', class_='wpbdp-field-business_website_address').a.text
            print(website)

        except Exception as e:
            website = 'none'

        csv_writer.writerow([website, company, category])

    if soup.select_one('.next a[href]'):
        soup = BeautifulSoup(requests.get(soup.select_one('.next a[href]')['href']).text, 'lxml')
        page += 1
    else:
        break