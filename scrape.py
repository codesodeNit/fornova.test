import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

url = "https://www.qantas.com/hotels/properties/18482?adults=2&checkIn=2023-10-30&checkOut=2023-10-31&children=0&infants=0&location=London%2C%20England%2C%20United%20Kingdom&page=1&payWith=cash&searchType=list&sortBy=popularity"

# Set up the Selenium webdriver
driver = webdriver.Chrome()  # You need to have the Chrome driver installed and in your PATH

# Load the page
driver.get(url)

# Wait for the dynamic content to load (adjust the timeout as needed)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div/div/div[1]/div[2]/div[9]/div/div[2]/div/div[1]')))

# Get the page source after the dynamic content has loaded
html_content = driver.page_source

# Close the browser
driver.quit()

# Parse the HTML content
soup = BeautifulSoup(html_content, 'html.parser')

rooms = soup.select('.css-du5wmh-Box.e1m6xhuh0')

# Create a CSV file and write header
csv_file_path = 'room_details.csv'
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(
        ['Room Name', 'Rate Name', 'Number of Guests', 'Cancellation Policy', 'Price', 'Is Top Deal', 'Currency'])

    # Iterate through each room and extract information
    for room in rooms:
        room_name = room.find('h3', class_='css-19vc6se-Heading-Heading-Text e13es6xl3').text.strip()
        rate_name = room.find('h3',
                              class_='css-10yvquw-Heading-Heading-Text e13es6xl3').text.strip()  # Assuming rate name is present in a different h3 tag
        guests = room.select_one('.css-dme7zc-Box-Flex.e1pfwvfi0 span.css-u2xec8-Text.e1j4w3aq0').text.strip().split()[
            -1]
        cancellation_policy = room.select_one('.css-feb59v-Box.e1m6xhuh0 button.css-12hhnd3.e1ucyleq0').text.strip()
        price = room.select_one('.css-48rito-Box.e1c6pi2o0 [data-testid="amount"]').text.strip()
        is_top_deal = 'Top Deal' in room.find('h3',
                                              class_='css-10yvquw-Heading-Heading-Text e13es6xl3').text.strip()  # Modify this condition based on the actual HTML structure
        currency = room.select_one('.css-17uh48g-Text.e1j4w3aq0').text.strip()

        # Write the data to the CSV file
        csv_writer.writerow([room_name, rate_name, guests, cancellation_policy, price, is_top_deal, currency])

print(f'Data has been scraped and saved to {csv_file_path}.')
