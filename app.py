from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Database setup
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS pets (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        type TEXT,
                        breed TEXT,
                        description TEXT,
                        contact_name TEXT,
                        contact_email TEXT,
                        contact_phone TEXT
                 
                    )''')
    conn.close()

# Home - show all pets
@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    pets = conn.execute('SELECT * FROM pets').fetchall()
    conn.close()
    return render_template('index.html', pets=pets)

# Add pet
@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        breed = request.form['breed']
        description = request.form['description']
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_phone = request.form['contact_phone']



        conn = sqlite3.connect('database.db')
        conn.execute('INSERT INTO pets (name, type, breed, description, contact_name, contact_email, contact_phone) VALUES (?, ?, ?, ?, ?, ?, ?)',
                     (name, type_, breed, description, contact_name,contact_email,contact_phone))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_pet.html')

# Edit pet
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_pet(id):
    conn = sqlite3.connect('database.db')
    if request.method == 'POST':
        name = request.form['name']
        type_ = request.form['type']
        breed = request.form['breed']
        description = request.form['description']
        contact_name = request.form['contact_name']
        contact_email = request.form['contact_email']
        contact_phone = request.form['contact_phone']

        conn.execute('UPDATE pets SET name=?, type=?, breed=?, description=?, contact_name=?, contact_email=?, contact_phone=? WHERE id=?',
                     (name, type_, breed, description, contact_name,contact_email,contact_phone, id))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    pet = conn.execute('SELECT * FROM pets WHERE id=?', (id,)).fetchone()
    conn.close()
    return render_template('edit_pet.html', pet=pet)

# Delete pet
@app.route('/delete/<int:id>')
def delete_pet(id):
    conn = sqlite3.connect('database.db')
    conn.execute('DELETE FROM pets WHERE id=?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
