from mmap import ALLOCATIONGRANULARITY
import warnings

import pandas as pd
import numpy as np
import scipy as sc

import matplotlib.pyplot as plt
import seaborn as sns

def movie_review(genre, year, rated):
    plt.style.use('fivethirtyeight')
    pd.set_option('display.max_rows', 50)
    pd.set_option('display.max_columns', 50)
    warnings.filterwarnings('ignore')

    users = pd.read_csv('data/users.dat', sep='::', names=['user_id', 'twitter_id']) 
  

    ratings = pd.read_csv('data/ratings.dat', sep='::', names=['user_id', 'movie_id', 'rating', 'rating_timestamp']).sort_values("rating_timestamp")
    ratings["rating_timestamp"] = pd.to_datetime(ratings["rating_timestamp"], unit='s')
 

    movies = pd.read_csv('data/movies.dat', sep='::', header=None, names=['movie_id', 'movie_title', 'genres'])
 

    movies_rating = (ratings.set_index("movie_id").join(movies.set_index("movie_id"),how="left"))
    dummies = movies_rating['genres'].str.get_dummies()
    tidy_movie_ratings = (pd.concat([movies_rating, dummies], axis=1).drop(["rating_timestamp", "genres"], axis=1))
    tidy_movie_ratings["production_year"] = tidy_movie_ratings["movie_title"].str[-5:-1]
    tidy_movie_ratings["movie_title"] = tidy_movie_ratings["movie_title"].str[:-7]
    tidy_movie_ratings.reset_index(inplace=True)



    cols = ["movie_title", "rating", "production_year", genre , "movie_id"]
    condition0 = tidy_movie_ratings["production_year"].astype(int) == year
    condition1 = tidy_movie_ratings[genre] == 1

    genre_name = (tidy_movie_ratings[cols][condition0 & condition1].drop(genre, axis=1))

    genre_name["year"] = genre_name['production_year'].astype(int)//1*1


    count_group = genre_name.groupby("movie_id").count()["rating"]

    movie_list = count_group[count_group > 10].index.values
    movie_list[:5]
    condition = genre_name["movie_id"].isin(movie_list)
    columns = ["movie_title", "year", "rating"]

    genre_filtered = genre_name[condition][columns]
    top_rate_by_year = (genre_filtered.groupby(["year", "movie_title"]).mean().sort_values(["year", "rating"],ascending=rated)
        .groupby(level=0, as_index=False).apply(lambda x: x.head() if len(x) >= 5 else x.head(1)).reset_index(level=0, drop=True)).round(2)
    return top_rate_by_year

def main():
    checking = True
    while(checking == True):
        print("Please enter a number between 1 and 15 for the following movie genres: Action = 1, Adventure = 2, Animation = 3, Comedy = 4, Crime = 5, Documentary = 6, Drama = 7, Fantasy = 8,  History = 9, Horror = 10, Musical = 11, Mystery = 12, Romance = 13, Sci-Fi = 14, Thriller = 15")
        genre=int(input())
        genre_check = True
        genre_stir = ""
        while(genre_check == True):
            if genre == 1:
                genre_stir = "Action"
            elif genre == 2:
                genre_stir = "Adventure"
            elif genre == 3:
                genre_stir = "Animation"
            elif genre == 4:
                genre_stir = "Comedy"
            elif genre == 5:
                genre_stir = "Crime"
            elif genre == 6:
                genre_stir = "Documentary"
            elif genre == 7:
                genre_stir = "Drama"
            elif genre == 8:
                genre_stir = "Fantasy"
            elif genre == 9:
                genre_stir = "History"
            elif genre == 10:
                genre_stir = "Horror"
            elif genre == 11:
                genre_stir = "Musical"
            elif genre == 12:
                genre_stir = "Mystery"
            elif genre == 13:
                genre_stir = "Romance"
            elif genre == 14:
                genre_stir = "Sci-Fi"
            elif genre == 15:
                genre_stir = "Thriller"
            else:
                print ("Please enter a number between 1 and 15")
                genre = int(input())
            if genre >=1 or genre <=16: 
                genre_check = False 
        print("Please enter a year from 1980 to 2021")
        year=int(input())
        year_check = True
        while (year_check == True):
            if year < 1980 or year > 2021:
                print ("Please enter a year between 1980 and 2021")
                year = int(input())
            else:
                year_check = False
        print("Would you like to see the best rated or worst rated? Enter 1 for best and 2 for worst.")
        rated=int(input())
        rated_check = True
        while (rated_check == True):
            if rated == 1:
                rated = False
                rated_check = False
            elif rated == 2:
                rated = True
                rated_check = False
            else:
                print ("Please enter either 1 for best or 2 for worse.")
                rated = int(input())
        
        x = movie_review(genre_stir,year,rated)
        print (x)
        print ("Would you like to see another review? Enter 1 for yes or 2 for no")
        again = int(input())
        
        if again != 1:
            checking = False

if __name__ == "__main__":
    main()
