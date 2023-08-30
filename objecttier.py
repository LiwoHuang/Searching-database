# File: objecttier.py
#
# objecttier
#
# Builds Movie-related objects from data retrieved through 
# the data tier.
#
# Original author:
#   Prof. Joe Hummel
#   U. of Illinois, Chicago
#   CS 341, Spring 2022
#   Project #02
#
import datatier


##################################################################
#
# Movie:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#
class Movie:
  def __init__(self, Movie_ID, Title, Release_Year):
    self._Movie_ID = Movie_ID
    self._Title = Title
    self._Release_Year = Release_Year

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year

##################################################################
#
# MovieRating:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Year: string
#   Num_Reviews: int
#   Avg_Rating: float
#
class MovieRating:
  def __init__(self, Movie_ID, Title, Release_Year, Num_Reviews, Avg_Rating):
    self._Movie_ID = Movie_ID
    self._Title = Title
    self._Release_Year = Release_Year
    self._Num_Reviews = Num_Reviews
    self._Avg_Rating = Avg_Rating

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Year(self):
    return self._Release_Year
  
  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating


##################################################################
#
# MovieDetails:
#
# Constructor(...)
# Properties:
#   Movie_ID: int
#   Title: string
#   Release_Date: string, date only (no time)
#   Runtime: int (minutes)
#   Original_Language: string
#   Budget: int (USD)
#   Revenue: int (USD)
#   Num_Reviews: int
#   Avg_Rating: float
#   Tagline: string
#   Genres: list of string
#   Production_Companies: list of string
#
class MovieDetails:
  def __init__(self, movie_ID, title, release_Date, runtime, original_Language, budget, revenue, num_Reviews, avg_Rating, tagline, genres, production_Companies):
    self._Movie_ID = movie_ID
    self._Title = title
    self._Release_Date = release_Date
    self._Runtime = runtime
    self._Original_Language = original_Language
    self._Budget = budget
    self._Revenue = revenue
    self._Num_Reviews = num_Reviews
    self._Avg_Rating = avg_Rating
    self._Tagline = tagline
    self._Genres = genres
    self._Production_Companies = production_Companies

  @property
  def Movie_ID(self):
    return self._Movie_ID

  @property
  def Title(self):
    return self._Title

  @property
  def Release_Date(self):
    return self._Release_Date
  
  @property
  def Runtime(self):
    return self._Runtime

  @property
  def Original_Language(self):
    return self._Original_Language

  @property
  def Budget(self):
    return self._Budget

  @property
  def Revenue(self):
    return self._Revenue
  
  @property
  def Num_Reviews(self):
    return self._Num_Reviews

  @property
  def Avg_Rating(self):
    return self._Avg_Rating

  @property
  def Tagline(self):
    return self._Tagline
  
  @property
  def Genres(self):
    return self._Genres

  @property
  def Production_Companies(self):
    return self._Production_Companies


##################################################################
# 
# num_movies:
#
# Returns: # of movies in the database; if an error returns -1
#
def num_movies(dbConn):
  try:
    sql = """SELECT count(*) FROM Movies;"""
  
    rows = datatier.select_one_row(dbConn, sql)
     
    return rows[0];
  except Exception as err:
    print("num_movies failed:", err)
    return -1


##################################################################
# 
# num_reviews:
#
# Returns: # of reviews in the database; if an error returns -1
#
def num_reviews(dbConn):
  try:
    sql = """SELECT count(*) FROM Ratings;"""
  
    rows = datatier.select_one_row(dbConn, sql)
     
    return rows[0];
  except Exception as err:
    print("num_reviews failed:", err)
    return -1


##################################################################
#
# get_movies:
#  
# gets and returns all movies whose name are "like"
# the pattern. Patterns are based on SQL, which allow
# the _ and % wildcards. Pass "%" to get all stations.
#
# Returns: list of movies in ascending order by name; 
#          an empty list means the query did not retrieve
#          any data (or an internal error occurred, in
#          which case an error msg is already output).
#
def get_movies(dbConn, pattern):
  try:
    sql = """select Movie_ID, Title, strftime('%Y', Release_Date) as year
             from Movies
             where Title like ?
              order by Movie_ID asc;"""
  
    rows = datatier.select_n_rows(dbConn, sql, [pattern])
    
    S_list = []
    for row in rows:
         moviesObject = Movie(row[0], row[1], row[2])
         S_list.append(moviesObject)
    return S_list
  except Exception as err:
    print("get_movies failed:", err)
    return None


##################################################################
#
# get_movie_details:
#
# gets and returns details about the given movie; you pass
# the movie id, function returns a MovieDetails object. Returns
# None if no movie was found with this id.
#
# Returns: if the search was successful, a MovieDetails obj
#          is returned. If the search did not find a matching
#          movie, None is returned; note that None is also 
#          returned if an internal error occurred (in which
#          case an error msg is already output).
#
def get_movie_details(dbConn, movie_id):
  try:
    sql1 = """select Movies.Movie_ID, Movies.Title, strftime("%Y-%m-%d", Movies.Release_Date) AS Date, Movies.Runtime, Movies.Original_Language, Movies.Budget, Movies.Revenue
              from Movies
              WHERE Movies.Movie_ID = ?
              
              ;"""
      
    sql2_1 = """select count(Ratings.Rating)
              from Ratings
              left join Movies on Movies.Movie_Id = Ratings.Movie_Id
              WHERE Movies.Movie_ID = ?
              
              ;"""

    sql2_2 = """select AVG(Ratings.Rating) AS average_rating
              from Ratings
              left join Movies on Movies.Movie_Id = Ratings.Movie_Id
              WHERE Movies.Movie_ID = ?
              
              ;"""
    
    sql3 = """select Movie_Taglines.Tagline
              from Movie_Taglines
              left join Movies on Movies.Movie_Id = Movie_Taglines.Movie_Id
              WHERE Movies.Movie_ID = ?
              
              ;"""        

    sql4 = """select Genres.Genre_Name
              from Movie_Genres
              join Genres on Movie_Genres.Genre_ID = Genres.Genre_ID
              left join Movies on Movies.Movie_Id = Movie_Genres.Movie_Id
              WHERE Movies.Movie_ID = ?
              
              ;"""

    sql5 = """select Companies.Company_Name
              from Movie_Production_Companies
              join Companies on Movie_Production_Companies.Company_ID = Companies.Company_ID
              left join Movies on Movies.Movie_Id = Movie_Production_Companies.Movie_Id
              WHERE Movies.Movie_ID = ?
              
              ;"""
  
    rows1 = datatier.select_one_row(dbConn, sql1, [movie_id])
    if (rows1 == ()):
      return None

    rows2_1 = datatier.select_one_row(dbConn, sql2_1, [movie_id])
    rows2_2 = datatier.select_one_row(dbConn, sql2_2, [movie_id])

    if (rows2_1 == () or rows2_1[0] == 0):
      review_ = 0
      _rating = 0
    else:
      review_ = rows2_1[0]
      _rating = rows2_2[0]
    
    rows3 = datatier.select_one_row(dbConn, sql3, [movie_id])
    if rows3 == ():
      T_agline = ""
    else:
      T_agline = rows3[0]

    rows4 = datatier.select_n_rows(dbConn, sql4, [movie_id])

    rows5 = datatier.select_n_rows(dbConn, sql5, [movie_id])


    Genres_list = []
    Companies_list = []

    if rows4 is None or len(rows4) == 0:
      pass
    else:  
      for i in rows4:
        Genres_list.append(i[0])

    if rows5 is None or len(rows5) == 0:
      pass
    else:    
      for j in rows5:
        Companies_list.append(j[0])

    Genres_list.sort()
    Companies_list.sort()

    movieDetails = MovieDetails(rows1[0], rows1[1], rows1[2], rows1[3], rows1[4], rows1[5], rows1[6], review_, _rating, T_agline, Genres_list, Companies_list)

    return movieDetails
      
  except Exception as err:
    print("get_movie_details failed:", err)
    return None

  # pass
         

##################################################################
#
# get_top_N_movies:
#
# gets and returns the top N movies based on their average 
# rating, where each movie has at least the specified # of
# reviews. Example: pass (10, 100) to get the top 10 movies
# with at least 100 reviews.
#
# Returns: returns a list of 0 or more MovieRating objects;
#          the list could be empty if the min # of reviews
#          is too high. An empty list is also returned if
#          an internal error occurs (in which case an error 
#          msg is already output).
#
def get_top_N_movies(dbConn, N, min_num_reviews):

  try:
    
    sql = """select Movies.Movie_ID, Movies.Title, strftime('%Y', Movies.Release_Date) as year, count(Ratings.Rating), AVG(Ratings.Rating) AS average_rating
            from Movies
            join Ratings on Movies.Movie_ID = Ratings.Movie_ID
            GROUP BY Ratings.Movie_ID
            HAVING COUNT(Rating) >= ?
            ORDER BY average_rating DESC
            limit ?;"""
  
    rows = datatier.select_n_rows(dbConn, sql, [min_num_reviews, N])

    S_list = []
    for row in rows:
         moviesObject = MovieRating(row[0], row[1], row[2], row[3], row[4])
         S_list.append(moviesObject)
    return S_list
  except Exception as err:
    print("get_top_N_movies failed:", err)
    return None


##################################################################
#
# add_review:
#
# Inserts the given review --- a rating value 0..10 --- into
# the database for the given movie. It is considered an error
# if the movie does not exist (see below), and the review is
# not inserted.
#
# Returns: 1 if the review was successfully added, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def add_review(dbConn, movie_id, rating):
  
  try:

    sql_id = """SELECT Movie_ID
            FROM Movies 
            WHERE Movie_ID = ?
            
            ;"""
    
    sql = """
            INSERT INTO Ratings (Movie_ID, Rating) VALUES (?, ?)
            ;"""

    name = datatier.select_one_row(dbConn, sql_id, [movie_id])
    if name == ():
      return 0
    
    rows = datatier.perform_action(dbConn, sql, [movie_id, rating])

    return rows

  except Exception as err:
    print("add_review failed:", err)
    return None


##################################################################
#
# set_tagline:
#
# Sets the tagline --- summary --- for the given movie. If
# the movie already has a tagline, it will be replaced by
# this new value. Passing a tagline of "" effectively 
# deletes the existing tagline. It is considered an error
# if the movie does not exist (see below), and the tagline
# is not set.
#
# Returns: 1 if the tagline was successfully set, returns
#          0 if not (e.g. if the movie does not exist, or if
#          an internal error occurred).
#
def set_tagline(dbConn, movie_id, tagline):
  try:

    sql_id = """SELECT Movie_ID
            FROM Movies 
            WHERE Movie_ID = ?
            
            ;"""

    sql_check = """SELECT Tagline
                  FROM Movie_Taglines 
                  WHERE Movie_ID = ?
            
                  ;"""
    
    sql1 = """
            UPDATE Movie_Taglines SET Tagline = ? WHERE Movie_ID = ?
            ;"""

    sql2 = """
            INSERT INTO Movie_Taglines (Movie_ID, Tagline) VALUES (?, ?)
            ;"""

    name = datatier.select_one_row(dbConn, sql_id, [movie_id])
    if name == ():
      return 0

    check = datatier.select_one_row(dbConn, sql_check, [movie_id])
    

    if check == ():
      rows = datatier.perform_action(dbConn, sql2, [movie_id, tagline])
    else:  
      rows = datatier.perform_action(dbConn, sql1, [tagline, movie_id])
    
    return rows

  except Exception as err:
    print("add_review failed:", err)
    return None
