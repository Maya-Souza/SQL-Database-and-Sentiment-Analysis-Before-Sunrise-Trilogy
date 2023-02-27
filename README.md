# 🎥 'Before Sunrise' trilogy IMDB audience reviews: did people's opinions of the 3 movies varied throughout the years? 🎥

The goal of this project was to run a sentiment analysis on IMDB audience reviews to get insights of people's perceptions of the three movies. The reviews were scraped, loaded into a SQL database and then made available through an API built using Flask for this project. Then the data was visualized by making API requests to my own database in order to see possible patterns in the audience's opinions.
Below, some contextualization, the step-by-step process, visualizations and conclusions.

![imagen](https://user-images.githubusercontent.com/109185207/221367485-ef9522f6-0467-46ee-9c2b-1dea7c33fdd7.png)


## Why do people might have heavily different opinions on movies depending on the year/decade they watch it?

It's fairly common to see a sharp difference in what the public thinks about a particular movie depending on when they have watched it. This might happen because certain latent topics that used to be even more overlooked and ignored back in the day - specially topics related to race, gender and sexuality - are now out in the open and the audience is more attentive to them. Or, it might be that the 'media style' simply changes from time to time and we don't perceive movies the same way after these changes happen. I will be using the Before Sunrise trilogy of movies to try to show this change as part of the fourth project for the ``Ironhack Data Analytics Bootcamp``.

A quick google search shows that even though Before Sunrise, the first movie of the trilogy, was a hit when it first came out in 1995, now it's seen as pretentious by many. Conversely, Before Midnight, the last one, was received as "overly 'woke'" by part of the audience when it came out in 2013.

With the analysis here presented I intend to check these differences throughout the years and see how people's opinions have changed since the movies' release dates in comparison to today by conducting a ``sentiment analysis`` on the audience reviews left on IMDB.

## Methodology and tools used

The step-by-step for this project was as it follows:

1. ``Gathering the data``. Here, I decided to scrape all the audience reviews left for the 3 movies on the IMDB website. In total, I scraped around 1500 reviews starting in 1998 (for the first movie) until 2022.  <br/>
                 <br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: I've used Selenium to load all the reviews and Scrapy to scrape them, all through Python. 
                    I've referenced this [*website*](https://www.analyticsvidhya.com/blog/2022/07/scraping-imdb-reviews-in-python-using-selenium/) to learn &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; how to use these two tools (which I hadn't learned before this) in this specific context. 

2. ``Running the Sentiment Analysis``. After scraping all the data and having it loaded into Pandas dataframes, I could check if each review was mainly positive, neutral or negative, along with their 'compound' metric. The compound score is a combination of the 3 possible classifications and varies from -1 to 1, 1 being completely positive and 0 being completely neutral. Theoretically, a sentence such as "This car is blue" would have a compound score of 0 since it doesn't contain adjectives, and therefore, lacks "feelings", it's simply stating a fact. After the analysis, I ended up with new columns in my dataframe with values for "positive", "neutral", "negative" and "compound" for each review. <br/>
<br/> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: The Python Natural Language Toolkit (NLTK) library.  

3. ``Designing a MySQL database and loading the data into it ``. Saving all the reviews I gathered in pickle or csv files would be possible, but for this project I actually designed a database which I could query by using MySQL. The data inserted is related to the reviews and the movies, so: name of the movie along with a unique id, name of the review's author and their id, the reviews themselves (plus the year and rating) and their ids, and finally, the results of the sentiment analysis run on them. I also added two extra tables: script and script_sentiment because as an idea for expanding this project I would like to run a sentiment analysis on the scripts for the movies and compare the results to the audience's reception of said movies. Below, the schema for the database I designed.  

      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: MySQL Workbench.  
      
   <img src= "https://user-images.githubusercontent.com/109185207/221370658-d657f078-53ff-44e0-a964-d95ca55b8c02.jpg" width="600" height="470">



4. ``Building an API to query the data``. Now that I had all the reviews scraped and loaded into my database, the next part was creating an API in order to make this data available through API requests. All the requests were queried through MySQL (the queries are available in the 'tools' folder) in order to give a response. For the purposes of this project, I developed the basic Flask app but did not deploy it, although this is something I want to do to complement it in the future. I've created 10 GET endpoints and 1 POST endpoint. These are:  

**GET REQUESTS**  

- @app.route("/") = access the README
- @app.route("/movies/") = lists all the movies in the database
- @app.route("/averages") = returns the average of ratings and coumpound sentiment for every movie
- @app.route("/averages/<movie_name>") = the averages for a specific movie
- @app.route("/moviesinfo/") = returns a dataframe with all the movies in the database and the average for sentiment analysis, number of reviews and ratings per year per movie
- @app.route("/moviesinfo/<movie_name>/") = the same as the previous one but for a specific movie
- @app.route("/reviews/<movie_name>") = returns all the reviews for a specific movie
- @app.route("/reviews/<movie_name>/<idreview>") = using the previous endpoint the user can choose an id and receive this specific review
- @app.route("/authors") = returns all the IMDB users that have left a review for any of the movies in the database (as of 2022)
- @app.route("/authors/<author_name>") = returns all the reviews made by a specific user  
  
  Below, an example of a get request:  
  <img src= "https://user-images.githubusercontent.com/109185207/221385920-3e0ab003-0b9b-4339-bdc8-9f840645c90f.jpg" width="600" height="470">

**POST REQUEST**
- @app.route("/newreview/", methods=["POST"]) = you can add your own review for a movie in the database (this review is not posted on IMDB) but it doesn't allow the same user to leave more than one review for the same movie. If the movie doesn't exist in the database, it is automatically added. The sentiment analysis is also automatically run and loaded into the database.  
  
params = {'author_name': '', 'movie_name': '', 'new_review': '', 'new_rating': , 'year': }  
  
  Below, an example of a post request:  
  <img src= "https://user-images.githubusercontent.com/109185207/221385906-54d9c77e-cd09-4e9f-be7f-0e5f020e4114.jpg" width="400" height="270">
 
  


5. ``Making requests to the API and visualizing the data``.

## Conclusions
