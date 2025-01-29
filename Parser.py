import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

def Parser():
    jobs = []
    # Set up Selenium WebDriver
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Run in headless mode (no browser UI)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    # URL of the page to scrape
    url = "https://the-trackr.com/uk-technology/"

    # Open the webpage
    driver.get(url)
    time.sleep(5)  # Wait for JavaScript to load the content

    # Extract page source and parse with BeautifulSoup
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()  # Close the browser

    # Locate the table
    table = soup.find("table", {"id": "table_1"})

    # Ensure table exists
    if not table:
        raise ValueError("Table not found! The webpage structure may have changed.")

    # Prepare CSV file
    csv_filename = "uk_tech_internships.csv"
    with open(csv_filename, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write CSV Header
        writer.writerow(
            ["Company Name", "Company Link", "Programme Name", "Programme Link", "Opening Date", "Closing Date"])

        # Extract table rows and write to CSV
        for row in table.find("tbody").find_all("tr"):
            cols = row.find_all("td")

            if len(cols) >= 4:  # Ensure there are enough columns
                company_name = cols[0].text.strip()
                company_link = cols[0].find("a")["href"] if cols[0].find("a") else ""

                programme_name = cols[1].text.strip()
                programme_link = cols[1].find("a")["href"] if cols[1].find("a") else ""

                opening_date = cols[2].text.strip()
                closing_date = cols[3].text.strip()

                writer.writerow(
                    [company_name, company_link, programme_name, programme_link, opening_date, closing_date])
                job = Job(company_name, company_link, programme_name, programme_link, opening_date, closing_date)
                jobs.append(job)

    print(f"Data successfully saved to {csv_filename}")
    return jobs

class Job:
    def __init__(self, company_name, company_link, programme_name, programme_link, opening_date, closing_date):
        self.company_name = company_name
        self.company_link = company_link
        self.programme_name = programme_name
        self.programme_link = programme_link
        self.opening_date = opening_date
        self.closing_date = closing_date

    def to_dict(self):
        """Converts the Job object to a dictionary format for JSON or UI rendering."""
        return {
            "company_name": self.company_name,
            "company_link": self.company_link,
            "programme_name": self.programme_name,
            "programme_link": self.programme_link,
            "opening_date": self.opening_date,
            "closing_date": self.closing_date
        }

    def __repr__(self):
        """Returns a string representation of the Job object."""
        return f"Job({self.company_name}, {self.programme_name}, {self.opening_date} - {self.closing_date})"

