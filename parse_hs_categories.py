import requests
import csv
from bs4 import BeautifulSoup


def get_html(url, params):
    response = requests.get(url, params=params)
    return response.text


def write_to_csv(rows):
    with open('hs_categories_classification.csv', 'a') as f:
        writer = csv.writer(f, delimiter=';')

        for row in rows:
            writer.writerow(row.values())


def process_category(url, html, categories_hieararchy):
    soup = BeautifulSoup(html, 'lxml')

    trs = soup.find(
        'div',
        class_='pad30'
    ).find('table').find_all('tr')

    for tr in trs:
        tds = tr.find_all('td')

        if len(tds) == 1:
            continue

        code = tds[0].text
        short_description = tds[1].text

        descr = {
            'code': code,
            'short_description': short_description
        }

        categories_hieararchy.append(descr)

        print(descr)

        if len(code) != 4:
            continue

        sub_category_html = get_html(url, params={'code': code})

        process_category(url, sub_category_html, categories_hieararchy)


def process_foreign_trade(url):
    category_count = 15

    for index in range(category_count):
        category = index + 1

        categories_hieararchy = []

        category_body_html = get_html(url, {'cat': category})

        process_category(url, category_body_html, categories_hieararchy)

        write_to_csv(categories_hieararchy)


if __name__ == '__main__':
    url = 'https://www.foreign-trade.com/reference/hscode.htm'
    process_foreign_trade(url)
