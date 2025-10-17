
def get_movies(conn, title, start_year, end_year, length, genre, rating, adult, sort_by, sorting, lim):
    cur = conn.cursor()

    query = """
        SELECT primarytitle, startyear, runtimeminutes, genres, averagerating, isadult
        FROM moviesimdb
        INNER JOIN ratings ON moviesimdb.tconst = ratings.tconst
    """

    conditions = []
    params = []

    if title:
        conditions.append("primarytitle ILIKE %s")
        params.append(f"%{title}%")
    if start_year:
        conditions.append("startyear >= %s")
        params.append(start_year)

    if end_year:
        conditions.append("startyear <= %s")
        params.append(end_year)

    if length:
        conditions.append("runtimeminutes <= %s")
        params.append(length)

    if genre:
        genres = [g.strip() for g in genre.split(",") if g.strip()]
        genre_conditions = []
        for g in genres:
            genre_conditions.append("genres ILIKE %s")
            params.append(f"%{g}%")
        if genre_conditions:
            conditions.append("(" + " AND ".join(genre_conditions) + ")")


    if rating:
        conditions.append("averagerating >= %s")
        params.append(rating)

    if adult:
        pass
    else:
        conditions.append("isadult = 0")

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    if sort_by != None and sorting:
        query += f" ORDER BY {sort_by} {sorting}"


    cur.execute(query, params)
    rows = cur.fetchmany(lim)
    cur.close()
    return rows

    