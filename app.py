from flask import Flask, request, render_template ,redirect, render_template_string
import hashlib
import time

app = Flask(__name__)


@app.route('/home', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        name = request.form['username']
        return f"Hello {name}, POST request received"
    return render_template('name.html')

if __name__ == '__main__':
    app.run(debug=True)