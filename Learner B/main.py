from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "movies_tv_guide.db"

def create_connection(db_file):
    """Creating the connection to the database and returns None if an error occurs"""
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return None

def search_movies_db(search_term):
    conn = create_connection(DATABASE)
    cur = conn.cursor()
    
    query = "SELECT title, type, genre_id, platform_id, year, rating, age_rating, runtime_mins, language FROM movies_tv_guide WHERE title LIKE ?"
    
    search = "%" + search_term + "%"
    
    cur.execute(query, (search,))
    
    movies_list = cur.fetchall()
    conn.close()
    
    print(movies_list)
    return movies_list

@app.route('/')
def render_index(): 
    return render_template('index.html')

@app.route('/all_movies') 
def render_all():
    query = "SELECT title, type, genre_id, platform_id, year, rating, age_rating, runtime_mins, language FROM movies_tv_guide"
    conn = create_connection(DATABASE) 
    cur = conn.cursor()

    cur.execute(query)
    movies_list = cur.fetchall()
    conn.close()

    print(movies_list)
    return render_template('all-movies.html', movies=movies_list)

@app.route('/search', methods=['POST'])
def search_route():
    search_term = request.form['search']
    
    movies_list = search_movies_db(search_term)
    
    return render_template('all-movies.html', movies=movies_list)

@app.route('/movie-maker') 
def render_movie_mkr():
    return render_template('movie-maker.html')

if __name__ == "__main__":
    app.run(debug=True)