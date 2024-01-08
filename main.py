 
# Import necessary libraries
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

# Create a Flask app
app = Flask(__name__)

# Define the database connection
conn = sqlite3.connect('andes_crashes.db')
c = conn.cursor()

# Define the main route
@app.route('/')
def index():
    # Query the database for all crashes
    crashes = c.execute('SELECT * FROM crashes').fetchall()

    # Render the index page with the list of crashes
    return render_template('index.html', crashes=crashes)

# Define the route for displaying crash details
@app.route('/crash_details/<crash_id>')
def crash_details(crash_id):
    # Query the database for the specific crash
    crash = c.execute('SELECT * FROM crashes WHERE id=?', (crash_id,)).fetchone()

    # Render the crash details page
    return render_template('crash_details.html', crash=crash)

# Define the route for handling search requests
@app.route('/search')
def search():
    # Get the search criteria from the request
    date_range = request.args.get('date_range')
    location = request.args.get('location')

    # Build the query based on the search criteria
    query = 'SELECT * FROM crashes'
    if date_range:
        query += ' WHERE date BETWEEN ? AND ?'
    if location:
        query += ' WHERE location LIKE ?'

    # Execute the query
    if date_range and location:
        crashes = c.execute(query, (date_range[0], date_range[1], '%' + location + '%')).fetchall()
    elif date_range:
        crashes = c.execute(query, (date_range[0], date_range[1])).fetchall()
    elif location:
        crashes = c.execute(query, ('%' + location + '%',)).fetchall()
    else:
        crashes = c.execute(query).fetchall()

    # Render the index page with the filtered crashes
    return render_template('index.html', crashes=crashes)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
