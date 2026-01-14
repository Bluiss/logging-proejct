from flask import Flask, request, render_template ,redirect, render_template_string
import hashlib
import time
import psycopg2
import dotenv, os
from dotenv import load_dotenv, dotenv_values 

load_dotenv()

# Get variables
HOSTNAME = os.getenv("HOSTNAME")
DATABASE = os.getenv("DATABASE")
USERNAME = 'postgres'
PWD = os.getenv("PWD")
PORT_ID = os.getenv("PORT_ID")



#SQL Statements
    
insert_data = """
                                INSERT INTO urls (original_url, short_code)
                                VALUES (%s, %s)
                                """
    
get_original_url = """
                        SELECT original_url FROM urls WHERE short_code=%s;
                        """

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        url = request.form['url']
    return render_template('name.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    original_url = request.form['url']

    # Create a unique hash for the original URL 
    unique_hash = hashlib.md5(f'{original_url}{time.time()}'.encode()).hexdigest()[:6]
    
    short_url = f'http://localhost:5000/{unique_hash}'

    try:
        conn = psycopg2.connect(
            host=HOSTNAME,
            dbname=DATABASE,
            user=USERNAME,
            password=PWD,
            port=PORT_ID
)
        
        cur = conn.cursor()
        cur.execute(insert_data, (original_url, unique_hash))
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        return f"Database error: {e}"
    
    return f'<h1>Shortened URL:</h1><a href="{short_url}">{short_url}</a>'



# Route to handle redirection to the original URL
@app.route('/<short_hash>')
def redirect_to_url(short_hash):
    try:
        # Connect to the database
        conn = psycopg2.connect(
            host=HOSTNAME,
            dbname=DATABASE,
            user=USERNAME,
            password=PWD,
            port=PORT_ID
        )
        cur = conn.cursor()

        # Fetch the original URL based on the short code
        cur.execute("SELECT original_url FROM urls WHERE short_code=%s", (short_hash,))
        result = cur.fetchone()

        cur.close()
        conn.close()
    except Exception as e:
        return f"Database error: {e}"

    if result:
        original_url = result[0]
        return redirect(original_url)
    else:
        return '<h1>404 - URL not found!</h1>', 404

if __name__ == '__main__':
    app.run(debug=True)