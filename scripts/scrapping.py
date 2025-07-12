# scripts/scraper.py

import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_URL = 'http://books.toscrape.com/'

def get_page_soup(url):
    response = requests.get(url)
    response.raise_for_status()
    return BeautifulSoup(response.text, 'html.parser')

def scrape_books():
    books = []
    page = 1

    while True:
        url = f"{BASE_URL}catalogue/page-{page}.html"
        try:
            soup = get_page_soup(url)
        except requests.exceptions.HTTPError:
            break  # No more pages

        for article in soup.select('article.product_pod'):
            title = article.h3.a['title']
            price_text = article.select_one('.price_color').text.strip()
            price_clean = price_text.encode('ascii', 'ignore').decode().replace('£', '').replace('Â', '').strip()
            price = float(price_clean)
            rating = article.p['class'][1]  # Example: 'Three'
            availability = article.select_one('.availability').text.strip()
            detail_url = BASE_URL + 'catalogue/' + article.h3.a['href']
            
            # Get Category and Image from detail page
            detail_soup = get_page_soup(detail_url)
            category = detail_soup.select('ul.breadcrumb li a')[-1].text.strip()
            image_url = BASE_URL + detail_soup.select_one('.item.active img')['src'].replace('../', '')

            books.append({
                'title': title,
                'price': float(price),
                'rating': rating,
                'availability': availability,
                'category': category,
                'image_url': image_url
            })

        page += 1

    # Save to CSV
    os.makedirs('data', exist_ok=True)
    df = pd.DataFrame(books)
    df['id'] = df.index + 1  # Add ID
    df.to_csv('data/books.csv', index=False)
    print(f"[✓] Extração finalizada: {len(df)} livros salvos em data/books.csv.")

if __name__ == "__main__":
    scrape_books()
