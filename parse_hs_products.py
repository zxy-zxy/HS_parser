import csv
import requests
from bs4 import BeautifulSoup


def write_to_csv(rows):
    with open('hs_products_classification.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')

        for row in rows:
            writer.writerow(row.values())


def parse_data(html):
    soup = BeautifulSoup(html, 'lxml')
    trs = soup.find(
        'table',
        id='hsCodeTable'
    ).find('tbody').find_all('tr')

    rows = []

    for tr in trs:
        tds = tr.find_all('td')

        rows.append(
            {
                'code': tds[0].text,
                'short_description': tds[1].text,
                'long_description': tds[2].text
            }
        )

    return rows


def get_html(url, params):
    response = requests.get(url, params=params)
    return response.text


def process_data(url, params):
    page_count = 376
    for page in range(page_count):
        params['d-7379888-p'] = page
        html = get_html(url, params)
        rows_to_csv = parse_data(html)
        write_to_csv(rows_to_csv)


if __name__ == '__main__':
    params = {
        'chapterCode': '',
        'headingCode': '',
        'longName': '',
        'sectionCode': '',
        'd-7379888-p': 1
    }

    url = 'https://mirsal2new.dubaitrade.ae/eMirsal/hsCodeSearch.do'
    process_data(url, params)
