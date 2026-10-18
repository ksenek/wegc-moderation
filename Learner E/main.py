from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)

DATABASE = "recipes.db"


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

@app.route('/')
def render_home():

    return render_template('index.html')

@app.route('/recipes')
def render_recipes():

    cuisine = request.args.get('cuisine', '')

    connection = create_connection(DATABASE)
    cursor = connection.cursor()

    if cuisine:
        query = """
        SELECT * FROM recipes
        WHERE cuisine = ?
        ORDER BY recipe_name
        """

        cursor.execute(query, (cuisine,))

    else:
        query = """
        SELECT * FROM recipes
        ORDER BY recipe_name
        """

        cursor.execute(query)

    recipes = cursor.fetchall()

    connection.close()

    return render_template(
        'recipes.html',
        recipes=recipes
    )

@app.route('/categories')
def render_categories():

    connection = create_connection(DATABASE)
    cursor = connection.cursor()

    query = """
    SELECT DISTINCT cuisine
    FROM recipes
    ORDER BY cuisine
    """

    cursor.execute(query)

    cuisines = cursor.fetchall()

    connection.close()

    return render_template(
        'categories.html',
        cuisines=cuisines
    )

@app.route('/category/<cuisine>')
def render_category(cuisine):

    connection = create_connection(DATABASE)
    cursor = connection.cursor()

    query = """
    SELECT * FROM recipes
    WHERE cuisine = ?
    ORDER BY recipe_name
    """

    cursor.execute(query, (cuisine,))

    recipes = cursor.fetchall()

    connection.close()

    return render_template(
        'recipes.html',
        recipes=recipes,
        page_title=cuisine + " Recipes"
    )

@app.route('/recipe/<int:recipe_id>')
def render_recipe_details(recipe_id):

    connection = create_connection(DATABASE)
    cursor = connection.cursor()

    query = """
    SELECT * FROM recipes
    WHERE id = ?
    """

    cursor.execute(query, (recipe_id,))

    recipe = cursor.fetchone()

    connection.close()

    return render_template(
        'recipe_details.html',
        recipe=recipe
    )

@app.route('/search')
def render_search():

    return render_template('search.html')

@app.route('/search-results')
def render_search_results():

    search = request.args.get('search', '')

    connection = create_connection(DATABASE)
    cursor = connection.cursor()

    query = """
    SELECT * FROM recipes
    WHERE recipe_name LIKE ?
    ORDER BY recipe_name
    """

    cursor.execute(query, ('%' + search + '%',))

    recipes = cursor.fetchall()

    connection.close()

    return render_template(
        'search_results.html',
        recipes=recipes,
        search=search
    )


if __name__ == '__main__':
    app.run(debug=True)