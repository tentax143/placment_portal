import os
import sys
import django

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "your_project.settings")  # Replace with your project settings
django.setup()

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
from datetime import datetime
from core_app.models import CoreJob  # Replace with your actual app name

options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--disable-software-rasterizer') 
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.3')

driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 2)  

try:
    driver.get("https://www.naukri.com/jobs-in-india?experience=0&functionAreaIdGid=3&functionAreaIdGid=4&functionAreaIdGid=5&functionAreaIdGid=7&functionAreaIdGid=8&functionAreaIdGid=30&functionAreaIdGid=36")

    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[1]/div[2]/div[1]/div[2]/span/div/button/span'))).click()
    time.sleep(3)  

    wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div/div/main/div[1]/div[2]/div[1]/div[2]/span/div/ul/li[2]/a'))).click()
    time.sleep(3)  

    today_date = datetime.now().strftime("%Y-%m-%d")
    count = 100  
    index, new_index, i = '0', 1, 0
    heading_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div/a'
    link_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div/a'
    subheading_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[2]//a'
    experience_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[3]/div/span[1]/span/span'
    salary_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[3]/div/span[2]/span/span'
    location_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[3]/div/span[3]/span/span'
    job_desc_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[4]/span'
    post_date_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[6]/span'
    image_xpath = '(//*[@class="srp-jobtuple-wrapper"])[' + index + ']/div/div[1]//img'

    while i < count:
        for j in range(20):
            temp_index = str(new_index).zfill(2)
            heading_xpath = heading_xpath.replace(index, temp_index)
            link_xpath = link_xpath.replace(index, temp_index)
            subheading_xpath = subheading_xpath.replace(index, temp_index)
            experience_xpath = experience_xpath.replace(index, temp_index)
            salary_xpath = salary_xpath.replace(index, temp_index)
            location_xpath = location_xpath.replace(index, temp_index)
            job_desc_xpath = job_desc_xpath.replace(index, temp_index)
            post_date_xpath = post_date_xpath.replace(index, temp_index)
            image_xpath = image_xpath.replace(index, temp_index)

            index = str(new_index).zfill(2)
            try:
                heading = wait.until(EC.presence_of_element_located((By.XPATH, heading_xpath))).text
                print(heading)
            except:
                heading = "NULL"
            try:
                link = wait.until(EC.presence_of_element_located((By.XPATH, link_xpath))).get_attribute('href')
                print(link)
            except:
                link = "NULL"
            try:
                subheading = wait.until(EC.presence_of_element_located((By.XPATH, subheading_xpath))).text
                print(subheading)
            except:
                subheading = "NULL"
            try:
                experience = wait.until(EC.presence_of_element_located((By.XPATH, experience_xpath))).text
                print(experience)
            except:
                experience = "NULL"
            try:
                salary = wait.until(EC.presence_of_element_located((By.XPATH, salary_xpath))).text
                print(salary)
            except:
                salary = "Not Disclosed"
            try:
                location = wait.until(EC.presence_of_element_located((By.XPATH, location_xpath))).text
                print(location)
            except:
                location = "NULL"
            try:
                job_desc = wait.until(EC.presence_of_element_located((By.XPATH, job_desc_xpath))).text
                print(job_desc)
            except:
                job_desc = "NULL"
            try:
                post_date = wait.until(EC.presence_of_element_located((By.XPATH, post_date_xpath))).text
                print(post_date)
            except:
                post_date = "NULL"
            try:
                image_link = wait.until(EC.presence_of_element_located((By.XPATH, image_xpath))).get_attribute('src')
                print(image_link)
            except:
                image_link = "NULL"

            new_index += 1
            i += 1
            print("--------------------------- " + str(i) + " ----------------------------------")

            # Use Django ORM to check for duplicates
            if not CoreJob.objects.filter(title=heading, company=subheading, link=link, 
                                           experience=experience, salary=salary, 
                                           location=location, description=job_desc).exists():
                # Create and save new job entry
                job = CoreJob(
                    title=heading,
                    company=subheading,
                    link=link,
                    experience=experience,
                    salary=salary,
                    location=location,
                    description=job_desc,
                    post_date=post_date,
                    image_link=image_link,
                    date_of_post=today_date
                )
                job.save()
                print("Inserted: ", heading)
            else:
                print("Duplicate found: ", heading)

            if i >= count:
                break
        if i >= count:
            break
        element = driver.find_element(By.XPATH, '//*[text() = "Next"]').location_once_scrolled_into_view
        driver.execute_script("window.scrollBy(0,-120)")
        wait.until(EC.element_to_be_clickable((By.XPATH, '//*[text() = "Next"]'))).click()
        new_index = 1

finally:
    driver.quit()
