import csv
from bs4 import BeautifulSoup
from selenium import webdriver

driver = webdriver.Chrome(executable_path="./chromedriver")


def get_url(search_term):
    template = 'https://www.amazon.com/s?k={}'
    search_term = search_term.replace(' ', '+')

    # Add Term Query To URL
    url = template.format(search_term)

    # Add Page Query Placeholder
    url += '&page={}'

    return url


def extract_record(item):
    tag = item.h2.a
    description = tag.text.strip()
    url = 'https://www.amazon.com' + tag.get('href')

    try:
        price = item.find('span', 'a-price').find('span', 'a-offscreen').text
    except AttributeError:
        return

    try:
        rating = item.i.text
        review_count = item.find('span', {'class': 'a-size-base', 'dir': 'auto'}).text
    except AttributeError:
        rating = ''
        review_count = ''

    image = item.find('img', {'class': 's-image'}).get('src')
    result = (description, price, rating, review_count, url, image)
    return result


'''Run Main Program Routine'''


def main(search_term):
    # Startup The Webdriver
    driver = webdriver.Chrome(executable_path="./chromedriver")

    records = []
    url = get_url(search_term)

    for page in range(1, 21):
        driver.get(url.format(page))
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        results = soup.find_all('div', {'data-component-type': 's-search-result'})

        for item in results:
            record = extract_record(item)
            if record:
                records.append(record)

    driver.close()

    # Save Results To CSV File
    with open('Results.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Description', 'Price', 'Rating', 'Reviews Count', 'URL', 'Image URL'])
        writer.writerows(records)


main('iphone 12')
