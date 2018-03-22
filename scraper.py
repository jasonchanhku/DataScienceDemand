from selenium import webdriver
import time

# get webdriver up and running
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
driver.get('https://www.glassdoor.com/index.htm')

# To type in job title and location
driver.find_element_by_css_selector('#KeywordSearch').send_keys('Housekeeper')
driver.find_element_by_css_selector('#LocationSearch').clear()
driver.find_element_by_css_selector('#LocationSearch').send_keys('Hong Kong')
driver.find_element_by_css_selector('#HeroSearchButton').click()


# Initializer for the while loop. Will be false once reaches end of page.
end = True

# Initialize lists to collect data
job_title = []
company = []
location = []
description = []
rating = []

while end:
    links = driver.find_elements_by_css_selector('#MainCol .flexbox .jobLink')

    for i,link in enumerate(links):
        time.sleep(2)
        link.click()
        print('Title: ', link.text)

        try:
            # to cancel the annoying pop up that tries to prevent scrapers
            driver.find_element_by_class_name('mfp-close').click()
        except:
            pass

        print('Company: ', link.find_elements_by_xpath('//div[@class="flexbox empLoc"]/div[1]')[i].text)
        # Below has issue, those ith HOT or NEW won't be read as posted date
        #print('Posted: ',link.find_elements_by_xpath('//span[@class="minor"]')[i].text)
        print('Link: ', link.find_elements_by_xpath('//div[@class="flexbox"]/div/a')[i].get_attribute('href'))
        time.sleep(10)

        try:
            print('Rating: ', link.find_element_by_xpath('//span[@class="compactStars margRtSm"]').text)
        except:
            print('Rating: NULL')
            pass

        try:
            print('Descrption: ',link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]').text)
        except:
            time.sleep(10)
            print('Descrption: ', link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]').text)
            pass
        print('\n')
        time.sleep(2)

    # To prevent selenium returning stalemate element
    # https://stackoverflow.com/questions/45002008/selenium-stale-element-reference-element-is-not-attached-to-the-page
    try:
        driver.find_element_by_css_selector('.next a').click()
    except:
        end = False
        break

print('Data successfully scraped')

time.sleep(5)
driver.close()

