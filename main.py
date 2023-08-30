
import sqlite3
import objecttier


##################################################################  
#
# print_stats
#

def print_stats(dbConn):
  
  m_ovies = objecttier.num_movies(dbConn)
  r_eviews = objecttier.num_reviews(dbConn)
  
  print(f"General stats:")
  print(f"  # of movies: {m_ovies:,}")
  print(f"  # of reviews: {r_eviews:,}")

##################################################################  
# 
# search_movies
# Command_1
# 

def Command_1(dbConn):
  print()
  name = input("Enter movie name (wildcards _ and % supported): ")
  print()
  movies = objecttier.get_movies(dbConn, name)

  if movies is None:  # error
    print("**Internal error: Command_1")
  elif len(movies) > 100:
    print("# of movies found:", len(movies))
    print()
    print("There are too many movies to display, please narrow your search and try again...")
  else:
    print("# of movies found:", len(movies))
    print()
    for s in movies:
      print(s.Movie_ID, ":", 
            s.Title,
           f"({s.Release_Year:})")

##################################################################  
# 
# search_movies_detail
# Command_2
#
def Command_2(dbConn):
  print()
  in_movie_id = input("Enter movie id: ")

  # name = "%matrix%"
  movies = objecttier.get_movie_details(dbConn, in_movie_id)

  if movies is None:  # error
    print()
    print("No such movie...")
  else:
    print()
    
    print(f"{movies.Movie_ID} : {movies.Title}")
    print(f"  Release date: {movies.Release_Date}")
    print(f"  Runtime: {movies.Runtime} (mins)")
    print(f"  Orig language: {movies.Original_Language}")
    print(f"  Budget: ${movies.Budget:,} (USD)")
    print(f"  Revenue: ${movies.Revenue:,} (USD)")
    print(f"  Num reviews: {movies.Num_Reviews}")
    print(f"  Avg rating: {movies.Avg_Rating:.2f} (0..10)")
    if (movies.Genres == []):
      print(f"  Genres: {', '.join(movies.Genres)}")
    else:
      print(f"  Genres: {', '.join(movies.Genres)},")
    
    if (movies.Production_Companies == []):
      print(f"  Production companies: {', '.join(movies.Production_Companies)}")
    else:
      print(f"  Production companies: {', '.join(movies.Production_Companies)},")
    print(f"  Tagline: {movies.Tagline}")


##################################################################  
# 
# Command_3
#
def Command_3(dbConn):
  print()
  in_N = input("N? ")
  if (int(in_N) <= 0):
    print("Please enter a positive value for N...")
    return None
  in_min_reviews = input("min number of reviews? ")
  if (int(in_min_reviews) <= 0):
    print("Please enter a positive value for min number of reviews...")
    return None
  
  movies = objecttier.get_top_N_movies(dbConn, int(in_N), int(in_min_reviews))

  if movies is None:  # error
    print()
    # print("No such movie...")
  else:
    print()
    for rating in movies:
      print(f"{rating.Movie_ID} : {rating.Title} ({rating.Release_Year}), avg rating = {rating.Avg_Rating:.2f} ({rating.Num_Reviews} reviews)")
    

##################################################################  
# 
# Command_4
#
def Command_4(dbConn):
  print()
  in_rating = input("Enter rating (0..10): ")
  if ((int(in_rating) < 0) or (int(in_rating) > 10)):
    print("Invalid rating...")
    return None
  in_id = input("Enter movie id: ")
  
  movies = objecttier.add_review(dbConn, in_id, int(in_rating))
  
  if movies == 0:  # error
    print()
    print("No such movie...")
  else:
    print()
    print("Review successfully inserted")

##################################################################  
# 
# Command_5
#
def Command_5(dbConn):
  print()
  in_tagline = input("tagline? ")

  in_id = input("movie id? ")
  
  movies = objecttier.set_tagline(dbConn, in_id, in_tagline)
  
  if movies == 0:  # error
    print()
    print("No such movie...")
  else:
    print()
    print("Tagline successfully set")
    
          
##################################################################  
#
# main
#
print('** Welcome to the MovieLens app **')

dbConn = sqlite3.connect('MovieLens.db')

print()

print_stats(dbConn)

print()
cmd = input("Please enter a command (1-5, x to exit): ")

while cmd != "x":
    if cmd == "1":
        Command_1(dbConn)
    elif cmd == "2":
        Command_2(dbConn)
    elif cmd == "3":
        Command_3(dbConn)
    elif cmd == "4":
        Command_4(dbConn)
    elif cmd == "5":
        Command_5(dbConn)
    else:
        print("**Error, unknown command, try again...")

    print()
    cmd = input("Please enter a command (1-5, x to exit): ")

dbConn.close()
#
# done
#