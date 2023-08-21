import requests
from bs4 import BeautifulSoup
import csv

# Set up the CSV file
csv_file = open('amazon_products.csv', 'w', newline='', encoding='utf-8')
csv_writer = csv.writer(csv_file)
csv_writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews',
                     'Description', 'ASIN', 'Product Description', 'Manufacturer'])

# Part1: Scraping Product Listings
for page_number in range(1, 21):
    url = f'https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_number}'

    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    product_listings = soup.find_all('div', class_='s-result-item')

    for listing in product_listings:
        product_url = listing.find('a', class_='a-link-normal')['href']
        product_name = listing.find('span', class_='a-size-medium').text.strip()
        product_price = listing.find('span', class_='a-offscreen').text.strip()

        rating_elem = listing.find('span', class_='a-icon-alt')
        rating = rating_elem.text.split()[0] if rating_elem else 'N/A'

        num_reviews_elem = listing.find('span', {'class': 'a-size-base', 'dir': 'auto'})
        num_reviews = num_reviews_elem.text if num_reviews_elem else '0'

        # Part 2: Scraping Product Details
        product_response = requests.get(product_url)
        product_soup = BeautifulSoup(product_response.content, 'html.parser')

        description = product_soup.find('meta', {'name': 'description'})['content']
        asin = product_soup.find('th', text='ASIN').find_next_sibling('td').text.strip()
        product_desc = product_soup.find('div', {'id': 'productDescription'}).text.strip()
        manufacturer = product_soup.find('a', {'id': 'bylineInfo'}).text.strip()

        csv_writer.writerow([product_url, product_name, product_price, rating, num_reviews,
                             description, asin, product_desc, manufacturer])

# Close the CSV file
csv_file.close()

print("Scraping and data export completed.")
