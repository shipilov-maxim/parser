import requests
from bs4 import BeautifulSoup
import json


def scrape_quotes():
    url = 'https://quotes.toscrape.com/'
    parsing_data = {}
    all_quotes = []
    page = 1

    while True:
        response = requests.get(url + f"page/{page}/")
        soup = BeautifulSoup(response.text, 'html.parser')
        quotes = soup.find_all('div', class_='quote')

        if not quotes:
            break

        for quote in quotes:
            text = quote.find('span', class_='text').get_text()
            author = quote.find('small', class_='author').get_text()
            tags = [tag.get_text() for tag in quote.find_all('a', class_='tag')]
            all_quotes.append({
                'text': text,
                'author': author,
                'tags': tags
            })

        page += 1

    parsing_data['items'] = all_quotes
    parsing_data['top_tags'] = [tag.find('a', class_='tag').get_text() for tag in
                                soup.find_all('span', class_='tag-item')]

    return parsing_data


if __name__ == '__main__':
    data = scrape_quotes()

    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    print('Цитаты успешно собраны и сохранены в data.json')
