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
    if not table:
        raise ValueError("Table not found! The webpage structure may have changed.")

    for row in table.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        flag = True
        if len(cols) >= 4:  # Ensure there are enough columns
            company_name = cols[0].text.strip()
            company_link = cols[0].find("a")["href"] if cols[0].find("a") else ""

            programme_name = cols[1].text.strip()
            programme_link = cols[1].find("a")["href"] if cols[1].find("a") else ""

            opening_date = cols[2].text.strip()
            closing_date = cols[3].text.strip()

            # Extract the additional fields (for example purposes, I'll assume the values are in specific columns)
            last_year_opening = cols[4].text.strip() if len(cols) > 4 else None
            cv_required = True if "CV required" in cols[
                5].text else False  # Assuming the cv_required field is based on some text
            cover_letter = cols[6].text.strip() if len(cols) > 6 else ""
            written_answers = True if "Written answers required" in cols[
                7].text else False  # Assuming this field has text indicators
            notes = cols[8].text.strip() if len(cols) > 8 else ""

            # Create the Job object with all the information
            job = Job(
                company_name,
                company_link,
                programme_name,
                programme_link,
                opening_date,
                closing_date,
                last_year_opening,
                cv_required,
                cover_letter,
                written_answers,
                notes
            )
            if programme_link == "":
                flag = False
            if company_name == "" and programme_name == "":
                flag = False
            if flag:
                jobs.append(job)
    return jobs

class Job:
    def __init__(self, company_name, company_link, programme_name, programme_link, opening_date, closing_date,
                 last_year_opening=None, cv_required=False, cover_letter="", written_answers=False, notes=""):
        self.company_name = company_name
        self.company_link = company_link
        self.programme_name = programme_name
        self.programme_link = programme_link
        self.opening_date = opening_date
        self.closing_date = closing_date
        self.last_year_opening = last_year_opening
        self.cv_required = cv_required
        self.cover_letter = cover_letter
        self.written_answers = written_answers
        self.notes = notes

    def to_dict(self):
        """Converts the Job object to a dictionary format for JSON or UI rendering."""
        return {
            "company_name": self.company_name,
            "company_link": self.company_link,
            "programme_name": self.programme_name,
            "programme_link": self.programme_link,
            "opening_date": self.opening_date,
            "closing_date": self.closing_date,
            "last_year_opening": self.last_year_opening,
            "cv_required": self.cv_required,
            "cover_letter": self.cover_letter,
            "written_answers": self.written_answers,
            "notes": self.notes
        }

    def __repr__(self):
        """Returns a string representation of the Job object."""
        return f"Job({self.company_name}, {self.programme_name}, {self.opening_date} - {self.closing_date})"
