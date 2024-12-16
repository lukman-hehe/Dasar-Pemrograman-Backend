from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

# Inisialisasi Flask dan MongoDB client
app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client['cruddb'] # Nama database
collection = db['users'] # Nama collection

# Route untuk menampilkan semua data
@app.route('/')
def index():
    users = collection.find() # Mengambil semua data
    return render_template('index.html', users=users)

# Route untuk menambah data
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        alamat = request.form['alamat']
        jurusan = request.form['jurusan']
        email = request.form['email']
        collection.insert_one({'name': name, 'alamat': alamat, 'jurusan': jurusan, 'email': email}) # Menambahkan data ke MongoDB
        return redirect(url_for('index'))
    return render_template('add.html')

# Route untuk mengedit data
@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    user = collection.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        name = request.form['name']
        alamat = request.form['alamat']
        jurusan = request.form['jurusan']
        email = request.form['email']
        collection.update_one({'_id': ObjectId(id)}, {'$set': {'name': name, 'alamat': alamat, 'jurusan': jurusan, 'email': email}})
        return redirect(url_for('index'))
    return render_template('edit.html', user=user)

# Route untuk menghapus data
@app.route('/delete/<id>')
def delete(id):
    collection.delete_one({'_id': ObjectId(id)})  # Menghapus data berdasarkan ID
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
