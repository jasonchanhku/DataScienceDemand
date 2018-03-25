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

        # Company Name
        print('Company: ', link.find_elements_by_xpath('//div[@class="flexbox empLoc"]/div[1]')[i].text)

        # Below has issue, those ith HOT or NEW won't be read as posted date
        #print('Posted: ',link.find_elements_by_xpath('//span[@class="minor"]')[i].text)

        # Link to the job
        print('Link: ', link.find_elements_by_xpath('//div[@class="flexbox"]/div/a')[i].get_attribute('href'))
        time.sleep(10)

        # Get Ratings
        try:
            print('Rating: ', link.find_element_by_xpath('//span[@class="compactStars margRtSm"]').text)
        except:
            print('Rating: NULL')
            pass

        # Tab 1: Job description
        try:
            print('Descrption: ',link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]').text)
        except:
            time.sleep(10)
            print('Descrption: ', link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]').text)
            pass

        # Tab 2: Company Tab
        driver.find_element_by_xpath('//li[@data-target = "CompanyContainer"]').click()
        print('Size: ', link.find_element_by_xpath('//div[@class = "info flexbox row"]/div[2]/span').text)
        print('Founded in: ', link.find_element_by_xpath('//div[@class = "info flexbox row"]/div[3]/span').text)
        print('Type: ', link.find_element_by_xpath('//div[@class = "info flexbox row"]/div[4]/span').text)
        print('Industry: ', link.find_element_by_xpath('//div[@class = "info flexbox row"]/div[5]/span').text)
        print('Revenue: ', link.find_element_by_xpath('//div[@class = "info flexbox row"]/div[6]/span').text)
        print('\n')

        # Tab 3: Rating Tab (only this tab needs try except)
        try:
            driver.find_element_by_xpath('//li[@data-target = "RatingContainer"]').click()
            print('CEO: ', link.find_element_by_xpath('//div[@class = "tbl gfxContainer"]/div[3]/div[@class="tbl"]/'
                                                      'div[2]/div[1]').text)
            print('Recommend: ', link.find_element_by_xpath('//div[@id = "EmpStats_Recommend"]').get_attribute('data-percentage'))
            print('Approve of CEO: ', link.find_element_by_xpath('//div[@id = "EmpStats_Approve"]').get_attribute('data-percentage'))
        except:
            # Put null for variables above
            print('NULL')



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

