from flask import Flask, request, render_template
import pymysql
from flask import redirect

app = Flask(__name__)

connection = pymysql.connect(host='localhost',
                             user='root', 
                             password='',  
                             database='perpus_nim')

@app.route('/')
def index():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM buku_nim")
        books = cursor.fetchall()
    return render_template('index_nim.html', books=books)

@app.route('/tambah', methods=['GET', 'POST'])
def tambah():
    if request.method == 'POST':
        kode_buku = request.form['kode_buku']
        nama_buku = request.form['nama_buku']
        penerbit = request.form['penerbit']
        pengarang = request.form['pengarang']
        jumlah_buku = request.form['jumlah_buku']
        
        with connection.cursor() as cursor:
            sql = "INSERT INTO buku_nim (Kode_Buku, Nama_Buku, Penerbit, Pengarang, Jumlah_Buku) VALUES (%s, %s, %s, %s, %s)"
            cursor.execute(sql, (kode_buku, nama_buku, penerbit, pengarang, jumlah_buku))
            connection.commit()
        return redirect('/')
    return render_template('tambah_nim.html')

@app.route('/edit/<kode_buku>', methods=['GET', 'POST'])
def edit(kode_buku):
    with connection.cursor() as cursor:
        if request.method == 'POST':
            nama_buku = request.form['nama_buku']
            penerbit = request.form['penerbit']
            pengarang = request.form['pengarang']
            jumlah_buku = request.form['jumlah_buku']
            
            sql = "UPDATE buku_nim SET Nama_Buku=%s, Penerbit=%s, Pengarang=%s, Jumlah_Buku=%s WHERE Kode_Buku=%s"
            cursor.execute(sql, (nama_buku, penerbit, pengarang, jumlah_buku, kode_buku))
            connection.commit()
            return redirect('/')
        
        cursor.execute("SELECT * FROM buku_nim WHERE Kode_Buku=%s", (kode_buku,))
        book = cursor.fetchone()
    return render_template('edit_nim.html', book=book)

@app.route('/hapus/<kode_buku>')
def hapus(kode_buku):
    with connection.cursor() as cursor:
        sql = "DELETE FROM buku_nim WHERE Kode_Buku=%s"
        cursor.execute(sql, (kode_buku,))
        connection.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)