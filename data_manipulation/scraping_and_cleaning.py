# Importing libraries

import pandas as pd
import numpy as np
import requests

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.select import Select

from scrapy.selector import Selector

from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import time
from tqdm import tqdm
import warnings
warnings.filterwarnings("ignore")

from selenium.webdriver.support.ui import WebDriverWait

#####################################
# FUNCTIONS #

def scraping_imdb_reviews(url):
    
    '''
    Function that receives a url of audience reviews from imdb and loads the page
    by clicking on the "load more" button (using Selenium) until all the reviews
    are loaded. Then, it scrapes all the reviews by using Scrapy and creates a pandas dataframe out of them.
    
    :args:

        url: the url for the review page
    
    :return:
        
        A dataframe with rating score, review title, author of the review, review url, the review
        itself and the review date.
      
    '''

    # Opening the page
    
    path = r"C:\Users\mayar\OneDrive\Área de Trabalho\chromedriver.exe"

    s = Service(path) #tell selenium to use Chrome and find the webdriver file in this location
    driver = webdriver.Chrome(service=s)  

    driver.get(url)


    #################################################################
    # Loading the page

    page = 1

    while page<50:  
        try:
            css_selector = 'load-more-trigger'
            driver.find_element(By.ID, css_selector).click()

            time.sleep(2)

            page+=1

        except:
            break

    #################################################################  
    # Scraping the reviews and loading them into a dataframe

    rating_list = []
    review_date_list = []
    review_title_list = []
    author_list = []
    review_list = []
    review_url_list = []
    error_url_list = []
    error_msg_list = []

    reviews = driver.find_elements(By.CSS_SELECTOR, 'div.review-container')

    for d in tqdm(reviews):
        try:
            sel2 = Selector(text = d.get_attribute('innerHTML'))
            try:
                rating = sel2.css('.rating-other-user-rating span::text').extract_first()
            except:
                rating = np.NaN
            try:
                review = sel2.css('.text.show-more__control::text').extract_first()
            except:
                review = np.NaN
            try:
                review_date = sel2.css('.review-date::text').extract_first()
            except:
                review_date = np.NaN    
            try:
                author = sel2.css('.display-name-link a::text').extract_first()
            except:
                author = np.NaN    
            try:
                review_title = sel2.css('a.title::text').extract_first()
            except:
                review_title = np.NaN
            try:
                review_url = sel2.css('a.title::attr(href)').extract_first()
            except:
                review_url = np.NaN
                
            rating_list.append(rating)
            review_date_list.append(review_date)
            review_title_list.append(review_title)
            author_list.append(author)
            review_list.append(review)
            review_url_list.append(review_url)
            
        except Exception as e:
            error_url_list.append(url)
            error_msg_list.append(e)

    review_df = pd.DataFrame({
        'Review_Date':review_date_list,
        'Author':author_list,
        'Rating':rating_list,
        'Review_Title':review_title_list,
        'Review':review_list,
        'Review_Url':review_url
        })
    
    return review_df

#####################################

def cleaning_reviews(reviews_df, name_movie):

    '''
    Function that receives a dataframe of IMDB audience reviews and
    cleans it so it can be loaded into a SQL database. It substitutes quotes, percent signs,
    line breaks and "None" for "Null. It also converts the review date column into datetime 
    and creates a new one with only the year. Lastly, it adds a column with the name of movie
    being reviewed.

    :args:
        reviews_df: the dataframe with the reviews.
        name_movie: the name of the movie.
    
    :return:
        the clean dataframe sorted by date.

    '''
    
    reviews_df['Review'] = reviews_df['Review'].str.replace("'","''") # This hasn't been refactored because I was receiving an error when I tried chaining it.
    reviews_df['Review'] = reviews_df['Review'].str.replace("\n"," ")
    reviews_df['Review'] = reviews_df['Review'].str.replace("%","%%")
    reviews_df['Review'] = reviews_df['Review'].str.replace('"',"''")
    
    reviews_df['Rating'][reviews_df['Rating'].isna()] = 'NULL'
    
    reviews_df['Review_Date'] = pd.to_datetime(reviews_df['Review_Date'])

    reviews_df.sort_values(by = 'Review_Date', inplace=True)
    reviews_df.reset_index(inplace=True, drop=True)
    
    reviews_df['Review_Year'] = pd.DatetimeIndex(reviews_df['Review_Date']).year
    
    reviews_df['Movie'] = name_movie

    
    return reviews_df

    
#####################################

   