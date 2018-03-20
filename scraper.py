from selenium import webdriver
import time
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
driver.get('https://www.glassdoor.com/index.htm')


driver.find_element_by_css_selector('#KeywordSearch').send_keys('Data Scientist')

driver.find_element_by_css_selector('#LocationSearch').clear()
driver.find_element_by_css_selector('#LocationSearch').send_keys('Hong Kong')

driver.find_element_by_css_selector('#HeroSearchButton').click()

num_pages = driver.find_elements_by_css_selector('.page a')
# print(len(links))
# driver.get(links[0].get_attribute('href'))

for num in range(len(num_pages)):

    links = driver.find_elements_by_css_selector('#MainCol .flexbox .jobLink')

    for link in links:
        time.sleep(2)
        link.click()
        time.sleep(2)
        try:
            # to cancel the annoying pop up that tries to prevent scrapers
            driver.find_element_by_class_name('mfp-close').click()
        except:
            None

    # To prevent selenium returning stalemate element
    # https://stackoverflow.com/questions/45002008/selenium-stale-element-reference-element-is-not-attached-to-the-page
    next = driver.find_element_by_css_selector('.next a')
    next.click()

time.sleep(5)
driver.close()

# To fix, there are actually > 4 pages upon reaching the 5th...
