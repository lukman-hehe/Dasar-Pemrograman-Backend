from flask import Flask, render_template, request, redirect, url_for, jsonify
import pymysql
import pymysql.cursors, os

application = Flask(__name__)

conn = cursor = None

# Fungsi koneksi database
def openDb():
    global conn, cursor
    conn = pymysql.connect(host="localhost", user="root", passwd="", database="stok")
    cursor = conn.cursor()

# Fungsi untuk menutup koneksi
def closeDb():
    global conn, cursor
    cursor.close()
    conn.close()

# Fungsi view index() untuk menampilkan data dari database
@application.route('/')
def index():
    openDb()
    container = []
    sql = "SELECT * FROM barang"
    cursor.execute(sql)
    results = cursor.fetchall()
    for data in results:
        container.append(data)
    closeDb()
    return render_template('index.html', container=container)

# Fungsi view untuk form tambah data
@application.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        openDb()
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        sql = "INSERT INTO barang (kodebrg, namabrg, harga, jumlah) VALUES (%s, %s, %s, %s)"
        val = (kode, nama, harga, jumlah)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        return render_template('tambah.html')

# Fungsi view edit() untuk menampilkan form edit dan mengubah data
@application.route('/edit/<id>', methods=['GET', 'POST'])
def edit(id):
    openDb()
    cursor.execute('SELECT * FROM barang WHERE id=%s', (id,))
    data = cursor.fetchone()
    if request.method == 'POST':
        kode = request.form['kode']
        nama = request.form['nama']
        harga = request.form['harga']
        jumlah = request.form['jumlah']
        sql = "UPDATE barang SET kodebrg=%s, namabrg=%s, harga=%s, jumlah=%s WHERE id=%s"
        val = (kode, nama, harga, jumlah, id)
        cursor.execute(sql, val)
        conn.commit()
        closeDb()
        return redirect(url_for('index'))
    else:
        closeDb()
        return render_template('edit.html', data=data)

# Fungsi view hapus() untuk menghapus data
@application.route('/hapus/<id>', methods=['GET', 'POST'])
def hapus(id):
    openDb()
    cursor.execute('DELETE FROM barang WHERE id=%s', (id,))
    conn.commit()
    closeDb()
    return redirect(url_for('index'))

if __name__ == '__main__':
    application.run(debug=True)
