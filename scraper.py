from selenium import webdriver
import time
import pandas as pd

# get webdriver up and running
options = webdriver.ChromeOptions()
options.add_argument('--incognito')
driver = webdriver.Chrome(options=options)
driver.get('https://www.glassdoor.com/index.htm')

# To type in job title and location
driver.find_element_by_css_selector('#KeywordSearch').send_keys('Data Scientist')
driver.find_element_by_css_selector('#LocationSearch').clear()
driver.find_element_by_css_selector('#LocationSearch').send_keys('Hong Kong')
driver.find_element_by_css_selector('#HeroSearchButton').click()

# Initializer for the while loop. Will be false once reaches end of page.
end = True

# Initialize lists to collect data before putting together a data frame
# Long term plan is to automate this with Morph.io and pull data using API
job_titles = []
companies = []
job_links = []
ratings = []
descriptions = []
sizes = []
founded_years = []
types = []
industries = []
revenues = []
CEOs = []
recommends = []
approves = []

cols = ['Title', 'Company', 'Link', 'Rating', 'Job_Description', 'Size', 'Founded', 'Company_Type', 'Industry',
        'Revenue', 'CEO', 'Recommend', 'Approve']

df = pd.DataFrame(columns=cols)

while end:
    links = driver.find_elements_by_css_selector('#MainCol .flexbox .jobLink')

    for i, link in enumerate(links):
        time.sleep(2)
        link.click()
        # Col 1: Job Title
        job_titles.extend([link.text])
        print('Title: ', job_titles[i])

        try:
            # to cancel the annoying pop up that tries to prevent scrapers
            driver.find_element_by_class_name('mfp-close').click()
        except:
            pass

        # Col 2: Company Name
        companies.extend([link.find_elements_by_xpath('//div[@class="flexbox empLoc"]/div[1]')[i].text])
        print('Company: ', companies[i])
        # Below has issue, those ith HOT or NEW won't be read as posted date
        # print('Posted: ',link.find_elements_by_xpath('//span[@class="minor"]')[i].text)

        # Col 3: Link to the job
        job_links.extend([link.find_elements_by_xpath('//div[@class="flexbox"]/div/a')[i].get_attribute('href')])
        time.sleep(5)

        # Col 4: Ratings
        try:
            ratings.extend([link.find_element_by_xpath('//span[@class="compactStars margRtSm"]').text])
            print('Ratings: ', ratings[i])
        except:
            ratings.extend([''])
            print('Ratings: ', ratings[i])
            pass

        # Tab 1: Job description
        # Col 5: Job description
        try:
            descriptions.extend([link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module '
                                                            'pad noMargBot"]').text])
        except:
            time.sleep(20)
            descriptions.extend([link.find_element_by_xpath('//div[@class="jobDescriptionContent desc module '
                                                            'pad noMargBot"]').text])
            pass

        # Tab 2: Company Tab
        # Successfully selected xpath same level based on condition
        try:
            driver.find_element_by_xpath('//li[@data-target = "CompanyContainer"]').click()

            # Col 6: Size
            sizes.extend([link.find_element_by_xpath('//div[@class = "infoEntity"][label[.] = "Size"]/'
                                                     'span[@class = "value"]').text])

            print('Size: ', sizes[i])

            # Col 7: Founded
            founded_years.extend([link.find_element_by_xpath('//div[@class = "infoEntity"][label[.] = "Founded"]/'
                                                             'span[@class = "value"]').text])

            print('Founded: ', founded_years[i])

            # Col 8: Type
            types.extend([link.find_element_by_xpath('//div[@class = "infoEntity"][label[.] = "Type"]/'
                                                     'span[@class = "value"]').text.strip("Company - ")])

            print('Type: ', types[i])

            # Col 9: Industry
            industries.extend([link.find_element_by_xpath('//div[@class = "infoEntity"][label[.] = "Industry"]/'
                                                          'span[@class = "value"]').text])

            print('Industry: ', industries[i])

            # Col 10: Revenue
            revenues.extend([link.find_element_by_xpath('//div[@class = "infoEntity"][label[.] = "Revenue"]/'
                                                        'span[@class = "value"]').text])
            print('Revenue: ', revenues[i])

        except:
            sizes.extend([''])
            print('Size: ', sizes[i])
            founded_years.extend([''])
            print('Founded: ', founded_years[i])
            types.extend([''])
            print('Type: ', types[i])
            industries.extend([''])
            print('Industry: ', industries[i])
            revenues.extend([''])
            print('Revenue: ', revenues[i])

            pass

        # Tab 3: Rating Tab (only this tab needs try except)
        try:
            driver.find_element_by_xpath('//li[@data-target = "RatingContainer"]').click()
            # Col 11: CEO
            CEOs.extend([link.find_element_by_xpath('//div[@class = "tbl gfxContainer"]/div[3]/div[@class="tbl"]'
                                                    '/div[2]/div[1]').text])
            print('CEO: ', CEOs[i])
            # Col 12: Recommend
            recommends.extend([link.find_element_by_xpath('//div[@id = "EmpStats_Recommend"]').
                              get_attribute('data-percentage')])
            print('Recommend: ', recommends[i])

            # Col 13: Approve of CEO
            approves.extend([link.find_element_by_xpath('//div[@id = "EmpStats_Approve"]').
                            get_attribute('data-percentage')])
            print('Approves: ', approves[i])
            print('\n')
        except:
            CEOs.extend([''])
            print('CEO: ', CEOs[i])
            recommends.extend([''])
            print('Recommend: ', recommends[i])
            approves.extend([''])
            print('Approves: ', approves[i])
            print('\n')
            pass

        df = df.append({

            'Title': job_titles[i],
            'Company': companies[i],
            'Link': job_links[i],
            'Rating': ratings[i],
            'Job_Description': descriptions[i],
            'Size': sizes[i],
            'Founded': founded_years[i],
            'Company_Type': types[i],
            'Industry': industries[i],
            'Revenue': revenues[i],
            'CEO': CEOs[i],
            'Recommend': recommends[i],
            'Approve': approves[i]

        }, ignore_index=True)

        time.sleep(2)

    # To prevent selenium returning stalemate element
    # https://stackoverflow.com/questions/45002008/selenium-stale-element-reference-element-is-not-attached-to-the-page
    try:
        driver.find_element_by_css_selector('.next a').click()
    except:
        end = False
        break

print('Data successfully scraped')

df.to_csv('glassdoor.csv', index=False)

print('Dataframe successfully constructed and saved')

time.sleep(5)
driver.close()
