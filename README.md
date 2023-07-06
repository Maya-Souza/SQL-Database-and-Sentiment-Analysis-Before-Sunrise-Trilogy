# 🎥 'Before Sunrise' trilogy IMDB audience reviews: did people's opinions of the 3 movies vary throughout the years? 🎥


The goal of this project was to run a sentiment analysis on IMDB audience reviews to get insights of people's perceptions of the three movies. The reviews were scraped, loaded into a SQL database and then made available through an API built using Flask for this project. Then the data was visualized by making API requests to my own database in order to see possible patterns in the audience's opinions.
Below you'll find some contextualization, the step-by-step process, visualizations and conclusions.

![imagen](https://user-images.githubusercontent.com/109185207/221367485-ef9522f6-0467-46ee-9c2b-1dea7c33fdd7.png)


## Why might people have heavily different opinions on movies depending on the year/decade they watch it?

It's fairly common to see a sharp difference in what the public thinks about a particular movie depending on when they have watched it. This might happen because certain latent topics that used to be even more overlooked and ignored back in the day - specially topics related to race, gender and sexuality - are now out in the open and the audience is more attentive to them. Or, it might be that the 'media style' simply changes from time to time and we don't perceive movies the same way after these changes happen. I will be using the Before Sunrise trilogy of movies to try to show this change as part of the fourth project for the ``Ironhack Data Analytics Bootcamp``.

A quick google search shows that even though Before Sunrise, the first movie of the trilogy, was a hit when it first came out in 1995, now it's seen as pretentious by many. Conversely, Before Midnight, the last one, was received as "overly 'woke'" by part of the audience when it came out in 2013.

With the analysis here presented I intend to check these differences throughout the years and see how people's opinions have changed since the movies' release dates in comparison to today by conducting a ``sentiment analysis`` on the audience reviews left on IMDB.  

![imagen](https://user-images.githubusercontent.com/109185207/221919338-c47f289b-ced8-4f14-83e7-4d19bff0a6e0.png)

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



4. ``Building an API to query the data``. Now that I had all the reviews scraped and loaded into my database, the next part was creating an API in order to make this data available through API requests. All the requests were queried through SQLAlchemy (the queries are available in the 'tools' folder) so I could build them through Python while connected to the MySQL database. For the purposes of this project, I developed the basic Flask app but did not deploy it, although this is something I want to do to complement it in the future.  
  
      &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: Flask, SQLAlchemy.

I've created 10 GET endpoints and 1 POST endpoint. These are:  

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
   

## API calls, visualizing the data and conclusions  
  
The goal of this analysis was to check if there's a clear difference between the ratings and sentiment from when each movie was released and now. With all the pieces done, I could call my own API so it would automatically query my data through MySQL and use the results to visualize it.  
  
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; *Tools*: My own API and Plotly for the visualizations.  
    
  <img src= "https://user-images.githubusercontent.com/109185207/221930192-880a930f-8f49-4695-8fe1-376c8124c0cb.jpg" width="700" height="270">  
  
  *The info needed for the visualizations being requested through the API*      
 
  --------   
    
  
    
1. I decided to check which of the movies had better ratings and if the sentiment analysis run on the reviews was indeed compatible with the average of ratings left by the users.   
  
  ![avg_all_ratings](https://user-images.githubusercontent.com/109185207/221914563-6dde725e-319b-41a2-9ef5-be6ef21e477c.jpeg)


- We can see that the first movie of the trilogy performed better than the other two and that the sentiment analysis seems to be consistent with the ratings results. It's worth mentioning that in order to leave a review, the user doesn't necessarily have to leave a rating. So, for some years, there are more reviews than ratings. With this piece of information only, it's not possible to verify how the audience's sentiment varied throughout the years, which brings us to the second visualization. 
  
  
2. The graphs below help us to find any possible differences in how the audiences perceived the movies depending on the year they watched them.  
    
  
  ![avg_sentiment_per_year_sunrise](https://user-images.githubusercontent.com/109185207/221914622-6aa42112-910c-4af6-b655-1fae9cb5285a.jpeg)

    
  
  ![avg_sentiment_per_year_sunset](https://user-images.githubusercontent.com/109185207/221914647-dec99cca-b9a8-4400-b82c-e30b7747221c.jpeg)

    
  
 
![avg_sentiment_per_year_midnight](https://user-images.githubusercontent.com/109185207/221914669-5c4f3b35-a580-41b9-8ce3-1d90e054f1d6.png)  
    
    
- There doesn't seem to be any visible trend in relation to people's opinions over the years. The fact the number of reviews can vary so drastically from one year to another also make it difficult to arrive at any conclusions. At first glance, it might look like people's sentiment changed a lot from one period to the next, but this happens only when the number of reviews is low, otherwise, the variation isn't that great.  
  
- An interesting thing is that all the movies experience a peak in reviews during 2020, most likely due to COVID, but even though the first movie reached 83 reviews, the second and the third ones reached around 40 each. This might be because people forgot or didn't want to leave reviews after the first one, or because they simply didn't like it and gave up on watching the whole trilogy.  
  
- Besides the pandemic years, there's also an increase of reviews in 2004/2005 and 2013/2014 for the first movie, and in 2013/2014 for the second one, probably because those are the years in which the second and the third movies, respectively, were released. It seems like people were watching the older movies before watching the most recent one. Similarly, the highest volume of reviews happens within the first 2 years of release date, except for Before Sunrise because it was released when the internet wasn't widespread.  
  
- Judging solely by the data shown in this analysis, a trend didn't become apparent. So, it's impossible to affirm that the public changed the way it looks at these movies depending on the year they watched them, specially because IMDb is not representative of every type of person that watched these trilogy. It could be interesting to replicate this analysis with movies that are more "controversial" or "problematic", such as comedies like "American pie". Or maybe complement these results with Tweets or Google Trends, for example, to see what people were and are saying about these movies online, outside of the "beaurocracy" of IMDb (having to create an account, leave a rating and write a review without any engagement from others with it).  
    
    
 **Thank you so much for reading, and if you have any comments or questions feel free to connect with me via [LinkedIn!](https://www.linkedin.com/in/mayara-almeida-souza/)**


  
