import os
from flask import Flask, render_template, request 
import sqlite3

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "Birds_Database.db")


#database connection function
def create_connection():
    try:
        conn = sqlite3.connect(DATABASE)
        return conn
    except sqlite3.Error as e:
        print("Database error:", e)
        return None

#homepage
@app.route("/")
def home():
    return render_template("index.html")


#birds page (list of all birds in database)

@app.route("/birds")
def birds():
    query = "SELECT bird_name, species_type, habitat, diet, region, size_category, max_wingspan_cm, conservation_status, max_lifespan_years, flight_ability, vocal_style, migratory FROM birds"

    


    con = create_connection()
    cur = con.cursor()
    cur.execute(query)
    bird_list = cur.fetchall()
    con.close()

    return render_template("birds.html", birds=bird_list)


#About page

@app.route("/about")
def about():
    return render_template("about_us.html")

#gallery page
@app.route("/gallery")
def gallery():
    
    return render_template("gallery.html")




@app.route("/search", methods=["POST"])
def search():
    keyword = request.form.get("search")
    
    con = create_connection()
    cur = con.cursor()
    
   
    query = """
    SELECT id, bird_name, species_type, habitat, diet, region, size_category,
           max_wingspan_cm, conservation_status, max_lifespan_years,
           flight_ability, vocal_style, migratory
    FROM birds 
    WHERE bird_name LIKE ? OR species_type LIKE ? OR habitat LIKE ?
"""

    
    cur.execute(query, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    results = cur.fetchall()
    con.close()
    
    return render_template("search_results.html", birds=results, search_term=keyword)




#run the app
if __name__ == "__main__":
    app.run(debug=True)
