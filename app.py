from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"  # Required for flashing messages

# Database initialization
def init_db():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE,
                    password TEXT NOT NULL
                )''')
    conn.commit()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        if not name or not email or not password:
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))

        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        # Check if the user already exists
        c.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = c.fetchone()

        if existing_user:
            flash('User already exists!', 'error')
            conn.close()
            return redirect(url_for('register'))

        # Save the new user
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        flash('Registration successful!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)