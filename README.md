# 'Before Sunrise' trilogy IMDB audience reviews: did people's opinions of the 3 movies varied throughout the years?

The goal of this project was to run a sentiment analysis on IMDB audience reviews to get insights of people's perceptions of the three movies. The reviews were scraped, loaded into a SQL database and then made available through an API built for this project. Then the data was visualized by making API requests to my own database in order to see possible patterns in the audience's opinions.
Below, some contextualization, the step-by-step process, visualizations and conclusions.

## Why do people might have heavily different opinions on movies depending on the year/decade they watch it?

It's fairly common to see a sharp difference in what the public thinks about a particular movie depending on when they have watched it. This might happen because certain latent topics that used to be even more overlooked and ignored back in the day - specially topics related to race, sexism and sexuality - are now out in the open and the audience is more attentive to them. Or, it might be that the 'media style' simply changes from time to time and we don't perceive movies the same way after these changes happen. I will be using the Before Sunrise trilogy of movies to try to show this change as part of the fourth project for the ``Ironhack Data Analytics Bootcamp``.

A quick google search shows that even though Before Sunrise, the first movie of the trilogy, was a hit when it first came out in 1995, now it's seen as pretentious by many. Conversely, Before Midnight, the last one, was received as "overly 'woke'" by part of the audience when it came out in 2013.

With the analysis here presented I intend to analyse these differences throughout the years and see how people's opinions have changed since the movies' release dates in comparison to today by conducting a ``sentiment analysis`` on the audience reviews left on IMDB.

## Methodology and tools used

The step-by-step for this project was as it follows:

1. ``Gathering the data``. Here, I decided to scrape all the audience reviews left for the 3 movies on the IMDB website. In total, I scraped around 1500 reviews starting in 1998 (for the first movie) until 2022.  <br/>
                 <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: I've used Selenium to load all the reviews and Scrapy to scrape them, all through Python. 
                    I've referenced this [*website*](https://www.analyticsvidhya.com/blog/2022/07/scraping-imdb-reviews-in-python-using-selenium/) to learn &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; how to use these two tools (which I hadn't learned before this) in this specific context. 

2. ``Running the Sentiment Analysis``. After scraping all the data and having it loaded into Pandas dataframes, I could check if each review was mainly positive, neutral or negative, along with their 'compound' metric. The compound score varies from -1 to 1, 1 being completely positive. <br/>
<br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: The Python Natural Language Toolkit (NLTK) library.  

3. ``Designing a SQL database and loading the data into it ``.

4. ``Building an API to query the data``.

5. ``Making requests to the API and visualizing the data``.

## Conclusions
