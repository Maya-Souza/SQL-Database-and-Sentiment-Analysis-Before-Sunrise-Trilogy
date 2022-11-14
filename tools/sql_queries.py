# Importing libraries #

import config.sql_connection as connect
import sqlalchemy as alch
import pandas as pd

engine = connect.connecting()


def check (table, string):
    
    '''
    Function that checks if a certain element is already in the database. It is called
    inside all of the "insert" query functions.
    
    :args:
        table: the name of the database table to be checked. It can assume the names "reviews",
        "movie", "review_author" or "review_sentiment"
        
        string: the element to be checked
    
    :return:
        True if the element exists in the table or False if it doesn't.
    
    
    '''
    
    if table == "reviews":
        query = list(engine.execute(f"SELECT review FROM reviews WHERE review = '{string}';"))
        if len(query) > 0:
            return True
        else:
            return False
        
    elif table == "movie":
        query = list(engine.execute(f"SELECT name FROM movie WHERE name = '{string}';"))
        if len(query) > 0:
            return True
        else:
            return False
        
    elif table == "review_author":
        query = list(engine.execute(f"SELECT name FROM review_author WHERE name = '{string}';"))
        if len(query) > 0:
            return True
        else:
            return False


    elif table == "review_sentiment":
        query1 = list(engine.execute(f"SELECT idauthor FROM review_author WHERE name = '{string}';"))[0]
        query = list(engine.execute(f"SELECT idreviews FROM reviews WHERE idauthor = '{query1}';"))
        if len(query) > 0:
            return True
        else:
            return False

################################################


def insert_movie(name_movie):

    '''
    Function that inserts a movie into the "movie" table.

    :args:
        name_movie
    '''
    
    if check("movie", name_movie):
        pass

    else:
        engine.execute(f"INSERT INTO movie (name) VALUES ('{name_movie}');")

################################################

def insert_author_from_df (col_authors):

    '''
    Function that inserts a author into the "review_author" table.

    :args:
        col_authors: the column "Author" from the reviews dataframe
    '''

    for row in col_authors:

        if check("review_author", row):
            print('Author already exists in database.')
            pass

        else:
            engine.execute(f"INSERT INTO review_author (name) VALUES ('{row}');")

################################################

def insert_author_from_api (author_name):
    
    if check("review_author", author_name):
        print('Author already exists in database.')
        pass
    
    else:
        engine.execute(f"INSERT INTO review_author (name) VALUES ('{author_name}');")

################################################

def insert_review (review_df):
    
    '''
    Function that inserts a review into the "reviews" table.

    :args:
        review_df: the reviews dataframe
    '''


    for index, row in review_df.iterrows():
    
        if check("reviews", row['Review']):
            pass
        
        else:
            qry = f"""
            INSERT INTO reviews (review, idmovie, year, rating, idauthor) 
            VALUES ('{row['Review']}', (SELECT idmovie FROM movie WHERE name = '{row['Movie']}'), 
            {row['Review_Year']}, {row['Rating']}, (SELECT idauthor FROM review_author WHERE name = '{row['Author']}'));
            """     
            engine.execute(qry)

################################################

def insert_review_sentiment(review_df):
    
    '''
    Function that inserts the sentiment analysis into the "review_sentiment" table.

    :args:
        review_df: the reviews dataframe
    '''
    
    for index, row in review_df.iterrows():
    
        if check("review_sentiment", row['Author']):
            pass
        
        else:
            qry = f"""
            INSERT INTO review_sentiment (pos, neg, neu, compound, idreviews) 
            VALUES ({row['positive sentiment']}, {row['negative sentiment']} , {row['neutral sentiment']}, 
            {row['compound sentiment']}, (SELECT idreviews FROM reviews WHERE review = '{row['Review']}'));
            """
            engine.execute(qry)


################################################

def sentiment_per_year(movie_name):

    '''
    Function that groups the tables reviwes and review_sentiment by year
    and movie and calculates the average of ratings, compound sentiment, 
    number of reviews and number of ratings.

    :args:
        movie_name: the name of the movie to have its information returned. 
        Type "all" to see the info for all the movies.

    :return:
        A dataframe with the information.
    
    '''
    
    qry1 = f"""
    SELECT r.year, m.name movie_name, AVG(rs.compound) avg_sentiment_compound, 
           AVG(rating) avg_rating, COUNT(r.rating) number_of_ratings, COUNT(r.idreviews) number_of_reviews
    FROM reviews r
    JOIN review_sentiment rs ON r.idreviews = rs.idreviews
    JOIN movie m ON r.idmovie = m.idmovie
    GROUP BY r.year, m.name
    """

    year_movie_compound_rating = pd.DataFrame(engine.execute(qry1))

    if movie_name == 'all':
        return year_movie_compound_rating
    
    elif check('movie', movie_name):
        return year_movie_compound_rating[year_movie_compound_rating['movie_name'] == movie_name]
    
    else:
        return 'Movie is not in database. Request with "all" to see all movies.'

################################################

def see_reviews(movie_name):
    
    qry = f"""
    SELECT r.idreviews, r.review, r.year, m.name movie_name, r.idauthor FROM reviews r
    JOIN movie m ON r.idmovie = m.idmovie
    WHERE m.name = '{movie_name}'
    """
    if check('movie', movie_name):
        return pd.DataFrame(engine.execute(qry))

    else:
        return 'Movie is not in database'

################################################

def see_specific_review(movie_name, idreview):
    
    qry = f"""
    SELECT r.idreviews, r.review, r.year, m.name movie_name, r.idauthor FROM reviews r
    JOIN movie m ON r.idmovie = m.idmovie
    WHERE m.name = '{movie_name}' AND r.idreviews = {idreview}
    """
    if check('movie', movie_name):
        
        query = list(engine.execute(f"SELECT review FROM reviews WHERE idreviews = '{idreview}';"))
        
        if len(query) > 0:
            return pd.DataFrame(engine.execute(qry))
        
        else:
            return 'No review with this id.'

    else:
        return 'Movie is not in database'

################################################

def see_specific_author(name_author):
    
    qry = f"""
    SELECT r.idreviews, r.review, r.year, m.name movie_name, r.idauthor, ra.name FROM reviews r
    JOIN movie m ON r.idmovie = m.idmovie
    JOIN review_author ra ON r.idauthor = ra.idauthor
    WHERE ra.name = '{name_author}'
    """
    if check('review_author', name_author):

        #query1 = list(engine.execute(f"SELECT ra.idauthor FROM ra WHERE ra.name = '{name_author}';"))[0]
        #query = list(engine.execute(f"SELECT review FROM reviews WHERE ra.idauthor = {query1};"))
   
        return pd.DataFrame(engine.execute(qry))

    else:
        return 'No review from this author.'

################################################

def new_review_or_movie(author_name, movie_name, new_review, new_rating, year):
    
    insert_movie(movie_name)
    insert_author_from_api(author_name)
    
    if (check('movie', movie_name) & check('review_author', author_name)):
        return 'A review for this movie has been posted by this user already'
    
    else:

        qry = f"""
        INSERT INTO reviews (idmovie, idauthor, review, rating, year) 
        VALUES (
            (SELECT idmovie FROM movie WHERE name = '{movie_name}'),
            (SELECT idauthor FROM review_author WHERE name = '{author_name}'),
            '{new_review}',
            {new_rating},
            {year}    
        ); 
        """

        engine.execute(qry)

        return 'Review inserted!'

################################################


def get_all_movies():

    a = pd.DataFrame(engine.execute("SELECT * FROM movie;"))

    return a 

################################################

def get_all_authors():

    a = pd.DataFrame(engine.execute("SELECT * FROM review_author;"))

    return a 
################################################

def get_averages(movie_name):

    if movie_name == 'all':
        qry = """
        SELECT AVG(r.rating) avg_all_ratings, AVG(rs.compound) avg_compound_sentiment, m.name
        FROM reviews r
        JOIN review_sentiment rs ON r.idreviews = rs.idreviews
        JOIN movie m ON r.idmovie = m.idmovie
        GROUP BY m.name
        """

        return pd.DataFrame(engine.execute(qry))
    
    elif check('movie', movie_name):
        
        qry = f"""
        SELECT AVG(r.rating) avg_all_ratings, AVG(rs.compound) avg_compound_sentiment, m.name
        FROM reviews r
        JOIN review_sentiment rs ON r.idreviews = rs.idreviews
        JOIN movie m ON r.idmovie = m.idmovie
        WHERE m.name = '{movie_name}'
        """
        return pd.DataFrame(engine.execute(qry)).to_json()
    
    elif check('movie', movie_name) == False:
        return "Movie not found."

################################################