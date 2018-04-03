# Data Science Demand in Hong Kong

![image](https://github.com/jasonchanhku/DataScienceDemand/blob/master/images/glassdoor.png)

This project aims to gauge the data science job demands in Hong Kong
in the past 30 days rolling based on job posts from Glassdoor. Glassdoor was 
the preferred data source because its wide array of available information:

* Job Title
* Company Name
* Link
* Company Rating
* Job Description
* Company Size
* Year Founded
* Company Type
* Industry
* Company Revenue
* CEO (sentiment)
* Recommend Percentage
* Approval Percentage

# Questions to be Answered

This project aims to answer the following questions:
* Who are hiring data scientists in Hong Kong ?
    * Big / small companies ?
    * What kind of industries ?
    * Good company feedback and approval ?
* Do company ratings differ from company types / industry / etc ?
* Given my preference of company type, which jobs suits me most ?


# Methodology
This project used a combination of Web Scraping, Exploratory Data Analysis (EDA)
and machine learning to answer the questions above.

## Automated Web Scraping
A script called `scraper.py` was written using `selenium` to handle web scraping the JavaScript heavy Glassdoor
website. The automation was done using a server space of [morph.io](www.morph.io). The automated scraper can be accessed
[here.](https://morph.io/jasonchanhku/DataScienceDemandScraper)

To manually run it on your local PC, just execute:

> python scraper.py

Do ensure that the requirements in `requirements.txt` are met.

This script will break if any of the website structure changes.

## Exploratory Data Analysis (EDA)

EDA of the data will be done and posted separately in a Jupyter notebook in this repository. In the EDA, the statistical
and visual elements of the data will be explored.

## Machine Learning

There are two ways machine learning can be applied for this project:

* Clustering of jobs into user preference of predictors
* Finding goodness of fit of user's CV and jobs available