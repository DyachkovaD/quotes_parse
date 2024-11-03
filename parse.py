import json
import requests
from bs4 import BeautifulSoup
import re

rezult = {'quotes': [], 'authors': []}
# url = 'https://quotes.toscrape.com/'


def find_quotes(quote_section):
    try:
        quote = {
            'text': quote_section.find('span', class_='text').text[1:-1],
            'author': quote_section.find('small', class_='author').text,
            'tags': [tag.text for tag in quote_section.find_all('a', class_='tag')],
        }

        rezult['quotes'].append(quote)

    except Exception as e:
        print(f"Error: {e}")


def find_authors(quote_section):
    author_url = quote_section.find('a', href=re.compile(r"^/author/")).get('href')

    try:
        author_response = requests.get(f"https://quotes.toscrape.com/{author_url}")
        author_soup = BeautifulSoup(author_response.text, 'html.parser')
        name = author_soup.find('h3', class_='author-title').text
        if name not in [aur.get('name') for aur in rezult.get('authors')]:
            author = {
                    'name': name,
                    'born_date': author_soup.find('span', class_='author-born-date').text,
                    'born_location': author_soup.find('span', class_='author-born-location').text,
                    'description': author_soup.find('div', class_='author-description').text.lstrip(" \n").rstrip(" \n"),
            }
            rezult['authors'].append(author)

    except Exception as e:
        print(f"Error: {e}")


for page_num in range(1, 11):
    url = f'https://quotes.toscrape.com/page/{page_num}/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    quotes = soup.select('.quote')
    for quote_section in quotes:
        find_quotes(quote_section)
        find_authors(quote_section)

with open("rezult.json", "w", encoding="utf-8") as file:
    json.dump(rezult, file, indent=4, ensure_ascii=False)
