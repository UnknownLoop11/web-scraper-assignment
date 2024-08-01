from bs4 import BeautifulSoup
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class Scraper:
    def __init__(self, url, num_projects=6):
        self.url = url
        self.num_projects = num_projects
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--log-level=3")
        self.driver = webdriver.Chrome(options=chrome_options)

    def destroy(self):
        """Explicitly close the WebDriver."""
        if self.driver:
            try:
                self.driver.quit()
            except Exception as e:
                logging.error(f"Error while closing the WebDriver: {e}")

    def scrape(self):
        """Returns the details of first 6 registered projects."""
        extracted_content = {}  # Dict to store the fully extracted data

        for index in range(self.num_projects):
            try:
                self.driver.get(self.url)
                self.driver.implicitly_wait(15)
                contents = self.driver.find_element(By.XPATH, '//*[@id="reg-Projects"]/div/div').find_elements(By.TAG_NAME, "a")


                contents[index].click()
                time.sleep(5)

                # Wait for the table to load and then extract the table data.
                content = self.driver.find_element(By.XPATH, '//*[@id="project-menu-html"]/div[2]/div[1]/div/table/tbody')
            except Exception as e:
                logging.error(f"Error while connecting to the website: {e}")
            else:
                soup = BeautifulSoup(content.get_attribute('innerHTML'), 'html.parser').find_all('tr')
                fields = ['Name', 'Permanent Address', 'PAN No.', 'GSTIN No.']  # Fields that are needed to be extracted
                scraped_data = {}
                for row in soup:
                    row_data = row.find_all('td')

                    if not row_data:
                        continue

                    key = row_data[0].text.strip()

                    # Checks if the current row contains the required fields to be extracted.
                    if key in fields:
                        if row_data[1].findNext('a') is not None:
                            row_data[1].findNext('a').decompose()  # Removes the anchor tag from the data
                        value = row_data[1].text.strip()
                        scraped_data[key] = value  # Adds the scraped data to the dictionary

                extracted_content[index] = scraped_data  # Adds the extracted data to the dictionary

        return extracted_content
