import data_manipulation.scraping_and_cleaning as d_m
import data_manipulation.sentiment_analysis as sent
import tools.sql_queries as sql

import pandas as pd



reviews_before_sunrise = d_m.scraping_imdb_reviews('https://www.imdb.com/title/tt0112471/reviews/?ref_=tt_ql_urv')
reviews_before_sunset = d_m.scraping_imdb_reviews('https://www.imdb.com/title/tt0381681/reviews/?ref_=tt_ql_urv')
reviews_before_midnight = d_m.scraping_imdb_reviews('https://www.imdb.com/title/tt2209418/reviews?ref_=tt_sa_3')

reviews_before_midnight = d_m.cleaning_reviews(reviews_before_midnight, 'Before Midnight')
reviews_before_sunset = d_m.cleaning_reviews(reviews_before_sunset, 'Before Sunset')
reviews_before_sunrise = d_m.cleaning_reviews(reviews_before_sunset, 'Before Sunrise')

reviews_before_sunrise = sent.sentiment_analysis_reviews(reviews_before_sunrise)
reviews_before_midnight = sent.sentiment_analysis_reviews(reviews_before_midnight)
reviews_before_sunset = sent.sentiment_analysis_reviews(reviews_before_sunset)

sql.insert_movie('Before Sunrise')
sql.insert_movie('Before Sunset')
sql.insert_movie('Before Midnight')

sql.insert_author_from_df(reviews_before_sunset['Author'])
sql.insert_author_from_df(reviews_before_sunrise['Author'])
sql.insert_author_from_df(reviews_before_midnight['Author'])

sql.insert_review(reviews_before_sunrise)
sql.insert_review(reviews_before_midnight)
sql.insert_review(reviews_before_sunset)

sql.insert_review_sentiment(reviews_before_sunrise)
sql.insert_review_sentiment(reviews_before_sunset)
sql.insert_review_sentiment(reviews_before_midnight)

