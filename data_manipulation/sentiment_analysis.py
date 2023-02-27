# Importing libraries
import numpy as np

import re

import spacy
import es_core_news_sm

import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

##### FUNCTION #####

def sentiment_analysis_reviews (reviews_df):

    '''
    Function that analyses the sentiment of each IMDB audience review by using the 
    Sentiment Intensity Analyzer from the NLTK library.

    :args:
        reviews_df: a dataframe with all the reviews.

    :return:
        the same dataframe but with 4 new columns: pos, neg, neu and compound.
    
    '''
    
    sia = SentimentIntensityAnalyzer()
    
    positive = []
    negative = []
    neutral = []
    compound = []
    
    for row in reviews_df['Review']:

        try:
            positive.append(sia.polarity_scores(row)['pos'])
            negative.append(sia.polarity_scores(row)['neg'])
            neutral.append(sia.polarity_scores(row)['neu'])
            compound.append(sia.polarity_scores(row)['compound'])

        except:
            positive.append(np.nan)
            negative.append(np.nan)
            neutral.append(np.nan)
            compound.append(np.nan)

    reviews_df['positive sentiment'] = positive
    reviews_df['negative sentiment'] = negative
    reviews_df['neutral sentiment'] = neutral
    reviews_df['compound sentiment'] = compound
        
    return reviews_df

##################################

   