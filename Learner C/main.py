"""This file connects the database to my website and executes queries."""
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "movie_tv_db/movies_tv2.db"


def create_connection(db_file):
    """Create connection to the database.

    :parameter db_file - the name of the file

    :returns connection - a connection to the database
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None


def get_filters():
    """Return filters and select distinct values from database."""
    con = create_connection(DATABASE)
    cur = con.cursor()

    query_genre_name = """SELECT DISTINCT genre.genre_name FROM movies_tv,
                         genre WHERE movies_tv.genre_id = genre.genre_id
                         ORDER BY genre_name"""
    query_type = "SELECT DISTINCT type FROM movies_tv ORDER BY type"
    query_age_rating = """SELECT DISTINCT age_rating.general_age_rating
                         FROM movies_tv, age_rating WHERE
                         movies_tv.age_rating_id = age_rating.age_rating_id
                         ORDER BY general_age_rating"""

    cur.execute(query_genre_name)
    genre_name = [record[0] for record in cur.fetchall()]

    cur.execute(query_type)
    type = [record[0] for record in cur.fetchall()]

    cur.execute(query_age_rating)
    general_age_rating = [record[0] for record in cur.fetchall()]

    con.close()

    return {"genre_name": genre_name, "type": type,
            "general_age_rating": general_age_rating}


@app.route('/')
def render_home():
    """Render index template."""
    con = create_connection(DATABASE)
    cur = con.cursor()

    query = "SELECT title FROM movies_tv"
    cur.execute(query)

    name_list = cur.fetchall()
    con.close()

    return render_template('index.html', names=name_list,
                           type="Homepage", filters=get_filters())


@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """Find all records which contain the search item.

    :POST contains the search value

    :returns a rendered page
    """
    search = request.form['search']
    title = f"Search results for '{search}'"
    query = """
            SELECT title, year, rating, runtime, genre.genre_name,
             age_rating.general_age_rating,
             platform.platform_name, language.language_name
             FROM movies_tv, genre, age_rating, platform, language
             WHERE movies_tv.genre_id = genre.genre_id AND
             movies_tv.age_rating_id = age_rating.age_rating_id AND
             movies_tv.platform_id = platform.platform_id AND
             movies_tv.language_id = language.language_id AND
             (title LIKE ? OR year LIKE ? OR rating LIKE ? OR runtime LIKE ?)
            """
    # checking if string is empty
    empty_search = search.isspace()
    if empty_search is True or len(list(search)) == 0:
        name_list = []

    elif empty_search is False:
        # removing whitespace
        search = search.strip()
        search = "%" + search + "%"

        con = create_connection(DATABASE)
        cur = con.cursor()
        cur.execute(query, (search, search, search, search))
        name_list = cur.fetchall()

        con.close()

    return render_template('movies_tv_shows.html',
                           names=name_list, title=title,
                           type="DisplayAll", filters=get_filters())


@app.route('/movies_tv_shows/<type>')
def render_movies_tv_shows(type):
    """Render movies_tv_shows."""
    filters = {
         'genre_name': request.args.get('genre_name'),
         'type': request.args.get('type'),
         'general_age_rating': request.args.get('general_age_rating')
    }

    filters = {k: v for k, v in filters.items() if v}

    query = """
        SELECT title, year, rating, runtime, genre.genre_name,
         age_rating.general_age_rating,
         platform.platform_name, language.language_name
         FROM movies_tv, genre, age_rating, platform, language
         WHERE movies_tv.genre_id = genre.genre_id AND
         movies_tv.age_rating_id = age_rating.age_rating_id AND
         movies_tv.platform_id = platform.platform_id AND
         movies_tv.language_id = language.language_id
    """
    params = []

    if type != "DisplayAll" and type != "ReleaseDates":
        query += " AND type = ?"
        params.append(type)

    if 'type' in filters:
        query += " AND type = ?"
        params.append(filters['type'])

    if 'genre_name' in filters:
        query += " AND genre.genre_name = ?"
        params.append(filters['genre_name'])

    if 'general_age_rating' in filters:
        query += " AND age_rating.general_age_rating = ?"
        params.append(filters['general_age_rating'])

    if type == "ReleaseDates":
        query += " ORDER BY year DESC"

    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, params)
    name_list = cur.fetchall()
    con.close()

    print(name_list)
    return render_template('movies_tv_shows.html', names=name_list,
                           title=type, type=type, filters=get_filters())


if __name__ == '__main__':
    app.run(debug=True)
