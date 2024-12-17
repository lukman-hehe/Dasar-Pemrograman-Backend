from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Tentukan folder untuk menyimpan file yang diupload
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Tentukan ekstensi file yang diizinkan
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'bmp'}

# Fungsi untuk memeriksa ekstensi file yang diupload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Periksa apakah file ada dalam request
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        # Jika tidak ada file yang dipilih
        if file.filename == '':
            return 'No selected file'
        # Jika file memiliki ekstensi yang diizinkan
        if file and allowed_file(file.filename):
            # Menyimpan file di folder uploads
            filename = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filename)
            return f'File successfully uploaded to {filename}'
        else:
            return 'Type File Tidak Sesuai, yang diperkenankan type (png, jpg, jpeg, gif, pdf, bmp)'
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
