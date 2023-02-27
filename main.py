import config.sql_connection as sql
import tools.sql_queries as queries
#import calling_functions 

import sqlalchemy as alch

import pandas as pd
import numpy as np

from flask import Flask, request
import markdown.extensions.fenced_code

#################################################


#sql.connecting()
#calling_functions()


#################################################

app = Flask(__name__)

# Render the markdwon
@app.route("/")
def readme ():
    readme_file = open("README.md", "r")
    return markdown.markdown(readme_file.read(), extensions = ["fenced_code"])

#################################################

@app.route("/moviesinfo/")
def info ():
    return (queries.sentiment_per_year('all')).to_json()
#################################################

@app.route("/moviesinfo/<movie_name>/")
def infospecificmovie (movie_name):
    return (queries.sentiment_per_year(movie_name)).to_json()
#################################################

@app.route("/movies/")
def get_movie ():
    return (queries.get_all_movies()).to_json()
#################################################

@app.route("/newreview/", methods=["POST"])
def try_post ():
    
    my_params = request.args
    author_name = my_params["author_name"]
    movie_name = my_params["movie_name"]
    new_review = my_params["new_review"]
    new_rating = my_params["new_rating"]
    year = my_params["year"]

    return(queries.new_review_or_movie(author_name, movie_name, new_review, new_rating, year))
#################################################

@app.route("/reviews/<movie_name>")
def get_movie_reviews (movie_name):
    return (queries.see_reviews(movie_name)).to_json()
#################################################

@app.route("/reviews/<movie_name>/<idreview>")
def get_specific_review (movie_name, idreview):
    return (queries.see_specific_review(movie_name, idreview)).to_json()
#################################################

@app.route("/authors/<author_name>")
def get_author (author_name):
    return (queries.see_specific_author(author_name)).to_json()
#################################################

@app.route("/authors")
def get_authors ():
    return (queries.get_all_authors()).to_json()

#################################################

@app.route("/averages")
def get_averages ():
    return (queries.get_averages('all')).to_json()

#################################################

@app.route("/averages/<movie_name>")
def get_averages_one_movie (movie_name):
    return (queries.get_averages(movie_name))

#################################################

if __name__ == "__main__":
    app.run(port=9000, debug=True)



