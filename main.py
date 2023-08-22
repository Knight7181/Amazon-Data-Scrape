import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from datetime import datetime


# Function to extract product title
def extract_product_title(soup):
    product_title_element = soup.find("span", attrs={"id": 'productTitle'})
    return product_title_element.text.strip() if product_title_element else None


# Function to extract product price
def extract_product_price(soup):
    product_price_element = soup.find('span', {'class': 'a-price-whole'})
    return product_price_element.text.strip() if product_price_element else None

# Function to extract product rating
def extract_product_rating(soup):
    product_rating_element = soup.find("span", attrs={"class": 'a-icon-alt'})
    return product_rating_element.text.strip() if product_rating_element else None

# Function to extract review count
def extract_review_count(soup):
    review_count_element = soup.find("span", attrs={"id": 'acrCustomerReviewText'})
    return review_count_element.text.strip() if review_count_element else None

# Function to extract product description
def extract_product_description(soup):
    product_description_element = soup.find("div", attrs={"id": 'productDescription'})
    return product_description_element.text.strip() if product_description_element else None

# Function to extract ASIN
def extract_asin(soup):
    asins = []
    for product in soup.find_all("div", {"data-asin": True}):
        asin = product["data-asin"]
        asins.append(asin)
    return asins

# Function to extract product manufacturer
def extract_manufacturer(soup):
    manufacturer_element = soup.find("a", attrs={"id": "bylineInfo"})
    return manufacturer_element.text.strip() if manufacturer_element else None


# Set up the WebDriver
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

URL = "https://www.amazon.in/s?k=ps5&crid=2F3FWY7X1TZF2&sprefix=ps5%2Caps%2C207&ref=nb_sb_noss_1"
###  The given URL was Giving error which I was not able to solve so I tried other  url of amazon product list and it works . Here is the product list of PS5

pages = 20

# Create a CSV file for output
current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
csv_filename = f"amazon_products_{current_time}.csv"

with open(csv_filename, mode='w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)

    # Write header row
    csv_writer.writerow(["Product Title", "Product Price", "Product Rating", "Number of Reviews",
                         "Product Description", "ASIN", "Product Manufacturer"])

    for page in range(1, pages + 1):
        page_url = f"{URL}&page={page}"
        driver.get(page_url)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        links = soup.find_all('a', attrs={
            'class': 'a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal'})

        for link in links:
            product_url = "https://amazon.in" + link.get('href')
            driver.get(product_url)
            product_page_source = driver.page_source
            product_soup = BeautifulSoup(product_page_source, 'html.parser')

            # Extract data using the defined functions
            product_title = extract_product_title(product_soup)
            product_price = extract_product_price(product_soup)
            product_rating = extract_product_rating(product_soup)
            review_count = extract_review_count(product_soup)
            product_description = extract_product_description(product_soup)
            asin = extract_asin(product_soup)
            manufacturer = extract_manufacturer(product_soup)

            # Write the product information to the CSV file
            csv_writer.writerow([product_title, product_price, product_rating, review_count,
                                 product_description, asin, manufacturer])

# Close the WebDriver
driver.quit()
