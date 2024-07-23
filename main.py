from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import chromedriver_autoinstaller
import time
import pandas as pd


class JobListing:
    def __init__(self, company, job_title, status, publishing_date, salary, location, job_description):
        self.company = company
        self.job_title = job_title
        self.status = status
        self.publishing_date = publishing_date
        self.salary = salary
        self.location = location
        self.job_description = job_description

    def __repr__(self):
        return f"JobListing({self.company}, {self.job_title}, {self.status}, {self.publishing_date}, {self.salary}, {self.location}, {self.job_description})"

def getDriver():
    opt = webdriver.ChromeOptions()
    opt.add_argument("--start-maximized")
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome(options=opt)
    return driver

def extract_job_details(job_card):
    try:
        company = job_card.find_element(By.CSS_SELECTOR, 'div.font-bold[data-v-c00a56b2]').text.strip()
    except:
        company = 'Unknown'
    try:
        job_title = job_card.find_element(By.CSS_SELECTOR, 'a.after\\:absolute.after\\:inset-0').text.strip()
    except:
        job_title = 'Unknown'
    try:
        status = job_card.find_element(By.CSS_SELECTOR, 'div[data-v-128b8421][class="truncate py-[2px]"]').text.strip()
    except:
        status = 'Unknown'
    try:
        publishing_date = job_card.find_element(By.CSS_SELECTOR, 'div[data-v-c00a56b2] time.text-sm').text.strip()
    except:
        publishing_date = 'Unknown'
    try:
        salary_element = WebDriverWait(job_card, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'span.flex.gap-2.items-center[data-v-c00a56b2] span.text-sm.truncate.w-full'))
        )
        salary = salary_element.text.strip()
    except:
        salary = 'Unknown'
    try:
        location = job_card.find_element(By.CSS_SELECTOR, 'span.flex.gap-2.items-start[data-v-c00a56b2] span.text-sm').text.strip()
    except:
        location = 'Unknown'
    try:
        job_description = job_card.find_element(By.CSS_SELECTOR, 'div.html-renderer.line-clamp-4.break-anywhere[data-v-c00a56b2]').text.strip()
    except:
        job_description = 'Unknown'

    return JobListing(company, job_title, status, publishing_date, salary, location, job_description)

try:
    driver = getDriver()
    driver.get("https://www.free-work.com/en-gb/tech-it/jobs")

    wait = WebDriverWait(driver, 30)
    time.sleep(5)  

    job_listings = []

    while True:
        job_cards = WebDriverWait(driver, 20).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div.mb-4.relative.rounded-lg.max-full.bg-white.flex.flex-col.cursor-pointer.shadow.hover\\:shadow-md'))
        )

        for job_card in job_cards:
            driver.execute_script("arguments[0].scrollIntoView(true);", job_card)
            job_listing = extract_job_details(job_card)
            job_listings.append(job_listing)

        try:
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.flex.items-center.gap-2.h-8.min-w-\\[2rem\\].px-3.inline-flex.items-center.justify-center.rounded-md.font-semibold.text-sm.border.border-transparent.outline-none.focus\\:outline-none.transition-all.duration-200.text-primary.bg-gray-100.hover\\:bg-gray-200'))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
            driver.execute_script("arguments[0].click();", next_button)
            time.sleep(5)  
        except Exception as e:
            print("No more pages or error navigating to the next page:", e)
            break

except Exception as ex:
    print(f"An error occurred: {ex}")

finally:
    if driver:
        driver.quit()

job_listings_dict = {
    'Company': [job.company for job in job_listings],
    'Job Title': [job.job_title for job in job_listings],
    'Status': [job.status for job in job_listings],
    'Publishing Date': [job.publishing_date for job in job_listings],
    'Salary': [job.salary for job in job_listings],
    'Location': [job.location for job in job_listings],
    'Job Description': [job.job_description for job in job_listings],
}

df = pd.DataFrame(job_listings_dict)

df.to_csv('job_listings.csv', index=False)

print("Job listings saved to job_listings.csv")

