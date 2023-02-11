from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException
import pandas as pd
from selenium.webdriver.chrome.options import Options

def fetch_jobs(keyword, num_pages):
    options = Options()
    options.add_argument("window-size=1920,1080")
    # Enter your chromedriver.exe path below
    chrome_path = "/Users/charanjeetkaur/Desktop/chromedriver 2.exe"
    driver = webdriver.Chrome(executable_path=chrome_path, options=options)
    driver.get("https://www.glassdoor.co.in/Job/Home/recentActivity.htm")
    search_input = driver.find_element(by=By.CSS_SELECTOR, value="#KeywordSearch")
    search_input.send_keys(keyword)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)

    company_name = []
    job_title = []
    salary_est = []
    location = []
    job_description = []
    salary_estimate = []
    company_size = []
    company_type = []
    company_sector = []
    company_industry = []
    company_founded = []
    company_revenue = []

    # Filtering job from last two weeks posted
    # try:
    # driver.find_element(by=By.CSS_SELECTOR, value="#filter_fromAge > span.css-1d8tv35.e16st97e0").click()
    # time.sleep(1)
    # except NoSuchElementException:
    # driver.find_element(by=By.CSS_SELECTOR, value="#PrimaryDropdown > ul > li:nth-child(5) > button > div").click()

    # Set current page to 1
    current_page = 1

    time.sleep(3)

    while current_page <= num_pages:

        done = False
        while not done:
            job_cards = driver.find_elements(by=By.XPATH,
                                             value="//article[@id='MainCol']//ul/li[@data-adv-type='GENERAL']")
            for card in job_cards:
                card.click()
                time.sleep(1)

                # Closes the signup prompt
                try:
                    driver.find_element(by=By.XPATH, value=".//span[@class='SVGInline modal_closeIcon']").click()
                    time.sleep(1)
                except NoSuchElementException:
                    time.sleep(1)
                    pass

                # Expands the Description section by clicking on Show More
                try:
                    driver.find_element(by=By.XPATH, value="//*[@id='JobDescriptionContainer']/div[2]").click()
                    time.sleep(2)
                except NoSuchElementException:
                    card.click()
                    print(str(current_page) + '#ERROR: no such element')

                    driver.find_element(by=By.XPATH, value="//*[@id='JobDescriptionContainer']/div[2]").click()
                except ElementNotInteractableException:
                    card.click()
                    driver.implicitly_wait(1)
                    print(str(current_page) + '#ERROR: not interactable')
                    driver.find_element(by=By.XPATH, value="//*[@id='JobDescriptionContainer']/div[2]").click()

                # Scrape

                try:
                    company_name.append(driver.find_element(by=By.XPATH,
                                                            value="//*[@id='JDCol']/div/article/div/div[1]/div/div/div[1]/div[3]/div[1]/div[1]/div").text)

                except:
                    company_name.append("#N/A")
                    pass

                try:
                    job_title.append(driver.find_element(by=By.XPATH,
                                                         value="//*[@id='JDCol']/div/article/div/div[1]/div/div/div/div/div[1]/div[2]").text)

                except:
                    job_title.append("#N/A")
                    pass

                try:
                    location.append(driver.find_element(by=By.XPATH,
                                                        value="//*[@id='JDCol']/div/article/div/div[1]/div/div/div/div/div[1]/div[3]").text)

                except:
                    location.append("#N/A")
                    pass

                try:
                    job_description.append(
                        driver.find_element(by=By.XPATH, value="//div[@id='JobDescriptionContainer']").text)

                except:
                    job_description.append("#N/A")
                    pass

                try:
                    salary_estimate.append(driver.find_element(by=By.XPATH,
                                                               value="//*[@id='JDCol']/div/article/div/div[2]/div[1]/div[2]/div/div/div[1]/div[1]").text)

                except:
                    salary_estimate.append("#N/A")
                    pass

                try:
                    company_size.append(driver.find_element(by=By.XPATH,
                                                            value="//*[@id='EmpBasicInfo']/div[1]/div/div[1]/span[2]").text)

                except:
                    company_size.append("#N/A")
                    pass

                try:
                    company_type.append(driver.find_element(by=By.XPATH,
                                                            value="//*[@id='EmpBasicInfo']/div[1]/div/div[2]/span[2]").text)

                except:
                    company_type.append("#N/A")
                    pass

                try:
                    company_sector.append(driver.find_element(by=By.XPATH,
                                                              value="//*[@id='EmpBasicInfo']/div[1]/div/div[4]/span[2]").text)

                except:
                    company_sector.append("#N/A")
                    pass

                try:
                    company_industry.append(driver.find_element(by=By.XPATH,
                                                                value="//*[@id='EmpBasicInfo']/div[1]/div/div[3]/span[2]").text)

                except:
                    company_industry.append("#N/A")
                    pass

                try:
                    company_founded.append(driver.find_element(by=By.XPATH,
                                                               value="//*[@id='EmpBasicInfo']/div[1]/div/div[2]/span[2]").text)

                except:
                    company_founded.append("#N/A")
                    pass

                try:
                    company_revenue.append(driver.find_element(by=By.XPATH,
                                                               value="//*[@id='EmpBasicInfo']/div[1]/div/div[6]/span[2]").text)

                except:
                    company_revenue.append("#N/A")
                    pass

                done = True

        # Moves to the next page
        if done:
            print(str(current_page) + ' ' + 'out of' + ' ' + str(num_pages) + ' ' + 'pages done')
            driver.find_element(by=By.XPATH, value="//span[@alt='next-icon']").click()
            current_page = current_page + 1
            time.sleep(4)

    driver.close()
    df = pd.DataFrame({'company': company_name,
                       'job title': job_title,
                       'location': location,
                       'job description': job_description,
                       'salary estimate': salary_estimate,
                       'company_size': company_size,
                       'company_type': company_type,
                       'company_sector': company_sector,
                       'company_industry': company_industry, 'company_founded': company_founded,
                       'company_revenue': company_revenue})

    df.to_csv(keyword + '.csv')
