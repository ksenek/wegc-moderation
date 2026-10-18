from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
DATABASE = "Recipes.db"

def create_connection(db_file):

    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
    return None

@app.route('/')
def render_home():
     query = """
SELECT r.recipe_name,
       r.main_ingredients,
       r.prep_time_min,
       r.cook_time_min,
       c.cuisine_name,
       dt.dietary_name,
       d.difficulty_name,
       r.img
FROM recipes r
JOIN cuisine c ON r.cuisine_id = c.cuisine_id
JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
JOIN difficulty d ON r.difficulty_id = d.difficulty_id
"""
     con = create_connection(DATABASE)
     cur = con.cursor()
    
     cur.execute(query)
     name_list = cur.fetchall()
     con.close()

     print(name_list)
     return render_template('index.html', names=name_list, title="All Recipes", filters=get_filters())

@app.route('/recipes')
def render_recipes():
    query = """
SELECT r.recipe_name,
       r.main_ingredients,
       r.prep_time_min,
       r.cook_time_min,
       c.cuisine_name,
       dt.dietary_name,
       d.difficulty_name,
       r.img
FROM recipes r
JOIN cuisine c ON r.cuisine_id = c.cuisine_id
JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
JOIN difficulty d ON r.difficulty_id = d.difficulty_id
"""
    con = create_connection(DATABASE)
    cur = con.cursor()

    filters = {
        "cuisine": request.args.get("cuisine"),
        "difficulty": request.args.get("difficulty"),
        "dietary": request.args.get("dietary")
    }

# Remove any empty filters
    filters = {k: v for k, v in filters.items() if v}
    
    cur.execute(query)
    name_list = cur.fetchall()
    con.close()

    print(name_list)
    return render_template('recipes.html', names = name_list, title="All Recipes", filters=get_filters())

@app.route('/search', methods=['GET', 'POST'])
def render_search():

    search = request.form['search']
    title = f"search for {search} from "
    query = """
SELECT r.recipe_name,
       r.main_ingredients,
       r.prep_time_min,
       r.cook_time_min,
       c.cuisine_name,
       dt.dietary_name,
       d.difficulty_name,
       r.img
FROM recipes r
JOIN cuisine c ON r.cuisine_id = c.cuisine_id
JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
JOIN difficulty d ON r.difficulty_id = d.difficulty_id
WHERE r.recipe_name LIKE ?
   OR r.main_ingredients LIKE ?
   OR r.prep_time_min LIKE ?
   OR r.cook_time_min LIKE ?
   OR c.cuisine_name LIKE ?
   OR dt.dietary_name LIKE ?
   OR d.difficulty_name LIKE ?
"""

    search = "%" + search + "%"

    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search, search, search, search, search))
    name_list = cur.fetchall()
    con.close()

    return render_template(
        "recipes.html",
        names=name_list,
        title=title,
        filters=get_filters())


def get_recipes(Recipes, filters=None):
    query = "SELECT recipe_name, main_ingredients, prep_time_min, cook_time_min FROM recipes WHERE cuisine_id = ?"
    params = [Recipes]

    if filters:

        if "cuisine" in filters:
            query += " AND cuisine_id=?"
            params.append(filters[cuisine_id])

        if "difficulty" in filters:
            query += " AND difficulty_id=?"
            params.append(filters[difficulty_id])

        if "dietary" in filters:
            query += " AND dietary_id=?"
            params.append(filters[dietary_tags_id])


    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, params)
    name_list = cur.fetchall()
    con.close()

    print(name_list)
    return name_list

def get_recipe_types():
    """returns something!"""
    con = create_connection(DATABASE)
    query = "SELECT DISTINCT cuisine_name FROM cuisine"

    cur = con.cursor()
    cur.execute(query)
    records = cur.fetchall()
    for i in range(len(records)):
        records[i] = records[i][0]
    return records

def get_filters():
    con = create_connection(DATABASE)
    cur = con.cursor()

    query_cuisine = "SELECT DISTINCT cuisine_name FROM cuisine ORDER BY cuisine_name"
    query_difficulty = "SELECT DISTINCT difficulty_name FROM difficulty ORDER BY difficulty_name"
    query_dietary = "SELECT DISTINCT dietary_name FROM dietary_tags ORDER BY dietary_name"

    cur.execute(query_cuisine)
    cuisine = [row[0] for row in cur.fetchall()]

    cur.execute(query_difficulty)
    difficulty = [row[0] for row in cur.fetchall()]

    cur.execute(query_dietary)
    dietary = [row[0] for row in cur.fetchall()]

    con.close()

    return {
        "cuisine": cuisine,
        "difficulty": difficulty,
        "dietary": dietary

    }

@app.route('/filter/cuisine')
def filter_cuisine():
    selected = request.args.get("cuisine", "")

    con = create_connection(DATABASE)
    cur = con.cursor()

    if selected:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min, c.cuisine_name,dt.dietary_name, d.difficulty_name, r.img
            FROM recipes r
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id
            WHERE c.cuisine_name = ?
            """, (selected,))
    else:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
            c.cuisine_name, dt.dietary_name, d.difficulty_name
            FROM recipes r 
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id""")

    name_list = cur.fetchall()
    con.close()

    return render_template("recipes.html",
                           names=name_list,
                           title=f"Cuisine: {selected if selected else 'All'}",
                           filters=get_filters())

@app.route('/filter/difficulty')
def filter_difficulty():
    selected = request.args.get("difficulty", "")

    con = create_connection(DATABASE)
    cur = con.cursor()

    if selected:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
                   c.cuisine_name, dt.dietary_name, d.difficulty_name, r.img
            FROM recipes r
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id
            WHERE d.difficulty_name = ?
        """, (selected,))
    else:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
                   c.cuisine_name, dt.dietary_name, d.difficulty_name
            FROM recipes r
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id
        """)

    name_list = cur.fetchall()
    con.close()

    return render_template("recipes.html",
                           names=name_list,
                           title=f"Difficulty: {selected if selected else 'All'}",
                           filters=get_filters())

@app.route('/filter/dietary')
def filter_dietary():
    selected = request.args.get("dietary", "")

    con = create_connection(DATABASE)
    cur = con.cursor()

    if selected:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
                   c.cuisine_name, dt.dietary_name, d.difficulty_name, r.img
            FROM recipes r
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id
            WHERE dt.dietary_name = ?
        """, (selected,))
    else:
        cur.execute("""
            SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
                   c.cuisine_name, dt.dietary_name, d.difficulty_name
            FROM recipes r
            JOIN cuisine c ON r.cuisine_id = c.cuisine_id
            JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
            JOIN difficulty d ON r.difficulty_id = d.difficulty_id
        """)

    name_list = cur.fetchall()
    con.close()

    return render_template("recipes.html",
                           names=name_list,
                           title=f"Dietary: {selected if selected else 'All'}",
                           filters=get_filters())

@app.route('/easyrecipes')
def easy_recipes():
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute("""
        SELECT r.recipe_name, r.main_ingredients, r.prep_time_min, r.cook_time_min,
        c.cuisine_name, dt.dietary_name, d.difficulty_name
        FROM recipes r
        JOIN cuisine c ON r.cuisine_id = c.cuisine_id
        JOIN dietary_tags dt ON r.dietary_tags_id = dt.dietary_tags_id
        JOIN difficulty d ON r.difficulty_id = d.difficulty_id
        WHERE d.difficulty_name = 'easy'""")

    name_list = cur.fetchall()
    con.close()

    return render_template("recipes.html", names=name_list, title="Easy", filters=get_filters())








