import os
import sqlite3
from flask import Flask, render_template, request, redirect, url_for, flash, session, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'supersecretkey'

# Create main upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- DB SETUP ---
def init_db():
    with sqlite3.connect('users.db') as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            )
        ''')
init_db()

# --- HELPER FUNCTIONS ---
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_user_folder(username):
    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], username)
    os.makedirs(user_folder, exist_ok=True)
    return user_folder

def get_file_info(filename, user_folder):
    filepath = os.path.join(user_folder, filename)
    return {
        'name': filename,
        'size': os.path.getsize(filepath),
        'path': filepath
    }

# --- ROUTES ---

@app.route('/')
def home():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = generate_password_hash(request.form['password'])

        try:
            with sqlite3.connect('users.db') as conn:
                conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
                flash('Registration successful! Please log in.')
                return redirect(url_for('login'))
        except sqlite3.IntegrityError:
            flash('Username already exists.')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password_input = request.form['password']

        with sqlite3.connect('users.db') as conn:
            user = conn.execute("SELECT * FROM users WHERE username = ?", (username,)).fetchone()

        if user and check_password_hash(user[2], password_input):
            session['username'] = username
            return redirect(url_for('dashboard'))
        flash('Invalid credentials.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('You have been logged out.')
    return redirect(url_for('login'))

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))

    username = session['username']
    user_folder = get_user_folder(username)

    if request.method == 'POST':
        # Handle file upload
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(user_folder, filename))
                flash(f'{filename} uploaded successfully.')
            else:
                flash('Invalid file or no file selected.')

    # Get search query from URL parameters
    search_query = request.args.get('search', '').lower()
    
    # Get sort parameter from URL
    sort_by = request.args.get('sort', 'name')  # Default sort by name
    
    # Get all files with their info
    files = []
    for filename in os.listdir(user_folder):
        if search_query and search_query not in filename.lower():
            continue
        files.append(get_file_info(filename, user_folder))
    
    # Sort files
    if sort_by == 'size':
        files.sort(key=lambda x: x['size'])
    else:  # Default sort by name
        files.sort(key=lambda x: x['name'].lower())

    return render_template(
        'index.html',
        files=files,
        username=username,
        search_query=search_query,
        current_sort=sort_by
    )

@app.route('/download/<filename>')
def download_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    filename = secure_filename(filename)
    user_folder = os.path.abspath(get_user_folder(session['username']))
    file_path = os.path.join(user_folder, filename)

    if not os.path.exists(file_path):
        flash('File does not exist.')
        return redirect(url_for('dashboard'))

    return send_from_directory(user_folder, filename, as_attachment=True)

@app.route('/delete/<filename>', methods=['POST'])
def delete_file(filename):
    if 'username' not in session:
        return redirect(url_for('login'))

    filename = secure_filename(filename)
    user_folder = get_user_folder(session['username'])
    filepath = os.path.join(user_folder, filename)

    try:
        os.remove(filepath)
        flash(f'{filename} deleted.')
    except FileNotFoundError:
        flash('File not found.')

    return redirect(url_for('dashboard'))

if __name__ == '__main__':
    app.run(debug=True)