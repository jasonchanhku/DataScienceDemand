from selenium import webdriver
import time


options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
driver.get('https://www.glassdoor.com/index.htm')


driver.find_element_by_css_selector('#KeywordSearch').send_keys('Housekeeper')

driver.find_element_by_css_selector('#LocationSearch').clear()
driver.find_element_by_css_selector('#LocationSearch').send_keys('Hong Kong')

driver.find_element_by_css_selector('#HeroSearchButton').click()

num_pages = driver.find_elements_by_css_selector('.page a')
# print(len(links))
# driver.get(links[0].get_attribute('href'))

end = True

while end:
    links = driver.find_elements_by_css_selector('#MainCol .flexbox .jobLink')

    for i,link in enumerate(links):
        time.sleep(2)
        link.click()
        print(link.text)
        try:
            # to cancel the annoying pop up that tries to prevent scrapers
            driver.find_element_by_class_name('mfp-close').click()
        except:
            None
        print(link.find_elements_by_xpath('//div[@class="flexbox empLoc"]/div')[i].text)

        time.sleep(10)
        print(link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module pad noMargBot"]').text)
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

# To fix, there are actually > 4 pages upon reaching the 5th...
