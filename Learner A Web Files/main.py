from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error


app = Flask(__name__)
DATABASE = "movies_tv_guide_db/movies_tv_guide.db"


def create_connection(db_file):
    """Creates connection to the database
    :parameter db_file - the name of the file
    :returns connection - a connection to the database"""

    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


def connect_to_db():
    conn = sqlite3.connect('movies_tv_guide_db/movies_tv_guide.db')
    cursor = conn.cursor()

    # 2. Store your SQL connection query in a string
    query = """
    SELECT 
        m.title, 
        g.genre, 
        p.platform, 
        m.year, 
        m.rating, 
        m.age_rating, 
        m.runtime_mins, 
        m.language, 
        m.poster
        FROM movies_tv_guide_table m
    INNER JOIN genre_table g ON m.genre_id = g.genre_id
    INNER JOIN platform_table p ON m.platform_id = p.platform_id;
    """

    # 3. Execute and fetch the results
    cursor.execute(query)
    results = cursor.fetchall()
    conn.close()
    return results


def get_media(media_type, filters=None):
    """Gets all media of a specific type from the database
    parameter = the type of media (Movie, TV Show)
    returns a list of media of that type.
    """
    clean_type = media_type.strip().lower()
    
    # 2. Force it to match your exact DB labels ("Movie" or "TV show")
    if "tv" in clean_type:
        search_value = "TV Show"
    else:
        search_value = "Movie"

    query = """
        SELECT m.title, g.genre, p.platform, m.year, m.rating, m.age_rating, m.runtime_mins, m.language, m.poster 
        FROM movies_tv_guide_table m
        INNER JOIN genre_table g ON m.genre_id = g.genre_id 
        INNER JOIN platform_table p ON m.platform_id = p.platform_id
        WHERE m.type = ?
    """
    params = [search_value]

    if filters:

        if "age_rating" in filters:
            query += " AND m.age_rating = ?"
            params.append(filters["age_rating"])

        if "year" in filters:
            query += " AND m.year = ?"
            params.append(filters["year"])

    con = create_connection(DATABASE)
    cur = con.cursor()


    cur.execute(query, params)
    name_list = cur.fetchall()
    con.close()


    print(name_list)
    return name_list


def get_filters():
    con = create_connection(DATABASE)
    cur = con.cursor()

    query_age_rating = "SELECT DISTINCT age_rating FROM movies_tv_guide_table ORDER BY age_rating"
    query_runtime_mins = "SELECT DISTINCT runtime_mins FROM movies_tv_guide_table ORDER BY runtime_mins"
    query_year = "SELECT DISTINCT year FROM movies_tv_guide_table ORDER BY year"

    cur.execute(query_age_rating)
    age_rating = [row[0] for row in cur.fetchall()]

    cur.execute(query_runtime_mins)
    runtime_mins = [row[0] for row in cur.fetchall()]

    cur.execute(query_year)
    year = [row[0] for row in cur.fetchall()]

    con.close()

    return {
        "age_rating": age_rating,
        "runtime_mins": runtime_mins,
        "year": year
    }


def get_media_types():

    con = create_connection(DATABASE)
    cur = con.cursor()


    query = "SELECT DISTINCT type FROM movies_tv_guide_table"
    cur.execute(query)


    records = cur.fetchall()


    print("Before flattening:", records)


    for i in range(len(records)):
        records[i] = records[i][0]


    print("After flattening:", records)
    return records


@app.route('/')
def render_home():
    all_media = connect_to_db()

    latest_movie = max(all_media, key=lambda x: x[3]) if all_media else None
    
    return render_template(
        'index.html', 
        names=all_media, 
        latest_movie=latest_movie,
        media_type=get_media_types(), 
        filters=get_filters()
    )

@app.route('/media/<media_type>')
def render_media(media_type):

    filters = {
        "genre" : request.args.get('genre'),
        "platform" : request.args.get('platform'),
        "year" : request.args.get('year')
    }

    filters = {k: v for k, v in filters.items() if v}

    return render_template(
        "media.html",
        names=get_media(media_type, filters),
        title=media_type.title(),
        media_type=get_media_types(),
        filters=get_filters()
    )


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form.get('search')
    if not search:
        search = ""

    age_rating_filter = request.form.get('age_rating')
    year_filter = request.form.get('year')

    title = "Search Results for '{search}'".format(search=search)

    query = """
        SELECT m.title, g.genre, p.platform, m.year, m.rating, m.age_rating, m.runtime_mins, m.language, m.poster 
        FROM movies_tv_guide_table m
        INNER JOIN genre_table g ON m.genre_id = g.genre_id
        INNER JOIN platform_table p ON m.platform_id = p.platform_id
        WHERE REPLACE(REPLACE(m.title || m.type || g.genre || p.platform || m.year || m.rating || m.age_rating || m.language, ' ', ''), '-', '') LIKE ?
    """

    cleaned_search = search.replace(" ", "").replace("-", "")
    wildcard_search = f"%{cleaned_search}%"

    params = [wildcard_search]

    # 2.  Age Rating filter if they picked one
    if age_rating_filter:
        query += " AND m.age_rating = ?"
        params.append(age_rating_filter)

    # 3.  Year filter if they picked one
    if year_filter:
        query += " AND m.year = ?"
        params.append(year_filter)

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, params)
    media_list = cur.fetchall()
    con.close()
    
    return render_template('media.html', names=media_list, title=title, media_type=get_media_types(), filters=get_filters())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

    
