# Movie Exploration System (PostgreSQL + Python CLI)

A PostgreSQL-based movie exploration system. The main focus of this project is on SQL data modeling, joins, filtering, and query optimization. A lightweight Python interface allows users to dynamically select genres, filter movies by year ranges, and sort movies based on rating, year, or title.

## Features

- Explore movies by genre and year range
- Sort movies dynamically by rating, release year, or title
- Fetch top-rated movies or movies within a specific time frame
- SQL-first approach with Python CLI interface
- Secure and parametrized queries to prevent SQL injection

## Database Setup

1. Create a PostgreSQL database named `moviesimdb`.
2. Import the cleaned movie titles data:

\copy moviesimdb(tconst, titletype, primarytitle, originaltitle, isadult, startyear, endyear, runtimeminutes, genres) FROM '/home/gasperh/Documents/movies_project/title.basics.cleaned.null.csv' WITH (FORMAT csv, HEADER true, NULL '\N');

3. Import the movie ratings data:

\copy ratings(tconst, averageRating, numVotes) FROM '/home/gasperh/Documents/movies_project/title.ratings.tsv' WITH (FORMAT csv, HEADER true, DELIMITER E'\t', NULL '\N');

4. Verify that the tables `moviesimdb` and `ratings` are populated correctly.

## Python Setup

1. Create a virtual environment:

python3 -m venv venv
source venv/bin/activate

2. Install required packages:

pip install psycopg2-binary tabulate

3. Run the CLI interface:

python3 -m app.main

## Project Structure

cinemadb/
│
├── app/
│   ├── main.py       # CLI interface
│   ├── db.py         # PostgreSQL connection setup
│   ├── queries.py    # SQL queries and dynamic filters
│
├── venv/             # Python virtual environment
└── README.md

## Usage

1. Start the CLI application.
2. Enter optional filters:
   - Genre
   - Start year / End year
   - Sort by (`rating`, `yearStart`, `titleOriginal`)
3. View results in a neatly formatted table in the terminal.

## Notes

- All SQL queries are parametrized for security.
- You can extend the filtering logic to include additional fields such as runtime, number of votes, or adult content.
- Sorting is only applied if the user selects a valid column; otherwise, the default order is used.

