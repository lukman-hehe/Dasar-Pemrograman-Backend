#import modul
import sqlite3

try:
    sqliteConnection = sqlite3.connect('pertemuan 10/database_siswa.db')
    cursor = sqliteConnection.cursor()
    print("Database Berhasil terkoneksi")
    # membuat tabel pada database
    sqlite_create_table_query = '''CREATE TABLE data_siswa (
        id INTEGER PRIMARY KEY,
        nama TEXT NOT NULL,
        email text NOT NULL UNIQUE);'''
    
    # eksekusi perintah sql
    cursor.execute(sqlite_create_table_query)
    sqliteConnection.commit()
    print("tabel berhasil di buat")
    sqlite_select_Query = "select sqlite_version();"
    cursor.execute(sqlite_select_Query)
    record = cursor.fetchall()
    print("SQLite Database Version is: ", record)
    cursor.close()
except sqlite3.Error as error:
    print("Error Gagal terkoneksi ke Database", error)
finally:
    if (sqliteConnection):
        sqliteConnection.close()
        print("Koneksi Database Selesai")
