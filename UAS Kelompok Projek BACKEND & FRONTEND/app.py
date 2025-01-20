# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import pymysql
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'bengkelmotorkey123'

def openDb():
    return pymysql.connect(
        host="localhost",
        user="root",
        passwd="",
        database="bengkel_motor"
    )

@app.route('/')
def index():
    return render_template('frontend/index.html')

@app.route('/catalog')
def catalog():
    conn = openDb()
    cursor = conn.cursor()
    
    selected_category = request.args.get('category', 'all')
    
    cursor.execute("SELECT DISTINCT kategori FROM spareparts ORDER BY kategori")
    categories = [row[0] for row in cursor.fetchall()]
    
    if selected_category and selected_category != 'all':
        cursor.execute("SELECT * FROM spareparts WHERE kategori=%s", (selected_category,))
    else:
        cursor.execute("SELECT * FROM spareparts")
    
    data = cursor.fetchall()
    conn.close()
    
    return render_template('frontend/catalog.html', 
                         spareparts=data, 
                         categories=categories,
                         selected_category=selected_category)

@app.route('/catalog/<int:id>')
def product_detail(id):
    conn = openDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spareparts WHERE id=%s", (id,))
    product = cursor.fetchone()
    conn.close()
    if product is None:
        flash('Produk tidak ditemukan', 'error')
        return redirect(url_for('catalog'))
    return render_template('frontend/product_detail.html', product=product)

@app.route('/admin')
def admin():
    conn = openDb()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM spareparts")
    total_spareparts = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM spareparts WHERE stok < 5")
    low_stock = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(stok) FROM spareparts")
    total_stock = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT * FROM spareparts WHERE stok < 5")
    low_stock_items = cursor.fetchall()
    
    cursor.execute("""
        SELECT kategori, COUNT(*) as count 
        FROM spareparts 
        GROUP BY kategori
    """)
    categories = [{"name": row[0], "count": row[1]} for row in cursor.fetchall()]
    
    conn.close()
    
    return render_template('backend/dashboard.html',
                         total_spareparts=total_spareparts,
                         low_stock=low_stock,
                         total_stock=total_stock,
                         low_stock_items=low_stock_items,
                         categories=categories)

@app.route('/admin/spareparts')
def admin_spareparts():
    conn = openDb()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM spareparts")
    data = cursor.fetchall()
    conn.close()
    return render_template('backend/spareparts/list.html', spareparts=data)

@app.route('/admin/spareparts/add', methods=['GET', 'POST'])
def admin_add_sparepart():
    if request.method == 'POST':
        kode = request.form['kode_part']
        nama = request.form['nama_part']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        
        if gambar:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{gambar.filename}"
            gambar.save(f"static/uploads/{filename}")
        else:
            filename = 'default.jpg'
            
        conn = openDb()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO spareparts 
            (kode_part, nama_part, harga, stok, gambar, deskripsi, kategori)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, (kode, nama, harga, stok, filename, deskripsi, kategori))
        conn.commit()
        conn.close()
        
        flash('Sparepart berhasil ditambahkan!', 'success')
        return redirect(url_for('admin_spareparts'))
        
    return render_template('backend/spareparts/add.html')

@app.route('/admin/sparepart/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit_sparepart(id):
    conn = openDb()
    cursor = conn.cursor()
    
    if request.method == 'POST':
        kode = request.form['kode_part']
        nama = request.form['nama_part']
        harga = request.form['harga']
        stok = request.form['stok']
        kategori = request.form['kategori']
        deskripsi = request.form['deskripsi']
        gambar = request.files['gambar']
        
        if gambar and gambar.filename:
            filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{gambar.filename}"
            gambar.save(f"static/uploads/{filename}")
            cursor.execute("""
                UPDATE spareparts 
                SET kode_part=%s, nama_part=%s, harga=%s, stok=%s, gambar=%s, 
                    deskripsi=%s, kategori=%s
                WHERE id=%s
            """, (kode, nama, harga, stok, filename, deskripsi, kategori, id))
        else:
            cursor.execute("""
                UPDATE spareparts 
                SET kode_part=%s, nama_part=%s, harga=%s, stok=%s, 
                    deskripsi=%s, kategori=%s
                WHERE id=%s
            """, (kode, nama, harga, stok, deskripsi, kategori, id))
        
        conn.commit()
        flash('Sparepart berhasil diupdate!', 'success')
        return redirect(url_for('admin_spareparts'))
    
    cursor.execute("SELECT * FROM spareparts WHERE id=%s", (id,))
    data = cursor.fetchone()
    conn.close()
    
    if data is None:
        flash('Sparepart tidak ditemukan', 'error')
        return redirect(url_for('admin_spareparts'))
        
    return render_template('backend/spareparts/edit.html', sparepart=data)

@app.route('/admin/sparepart/delete/<int:id>')
def admin_delete_sparepart(id):
    conn = openDb()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM spareparts WHERE id=%s", (id,))
    conn.commit()
    conn.close()
    flash('Sparepart berhasil dihapus!', 'success')
    return redirect(url_for('admin_spareparts'))

if __name__ == '__main__':
    app.run(debug=True)