from app.db import get_connection
from app.queries import get_movies
from decimal import Decimal
from tabulate import tabulate


def main():
    conn = get_connection()

    title = input("Title: ")
    start_year = input("From Year: ")
    end_year = input("To Year: ")
    length = input("Length (minutes): ")
    genre = input("Genre: ")
    rating = input("Lowest rating: ")
    adult = input("Include adult content? (y/n): ").lower() == 'y'

    allowed_sort = ["startyear", "runtimeminutes", "averagerating"]
    sort_by = input("Sortiraj po (startyear/runtimeminutes/averagerating): ")
    if sort_by not in allowed_sort:
        sort_by = None

    lim = input("Max results (default 10): ")
    if not lim.isdigit():
        lim = 10
    else:
        lim = int(lim)

    movies = get_movies(conn, title, start_year, end_year, length, genre, rating, adult, sort_by, lim)
    for movie in movies:
        movie = tuple(float(x) if isinstance(x, Decimal) else x for x in movie)
        #print(movie)

    titles = ["Title", "Year", "Length (minutes)", "Genres", "Rating", "Adult content"]
    print(tabulate(movies, headers=titles, tablefmt="grid"))
    

    conn.close()

if __name__ == "__main__":
    main()

#zobo!! takoj
