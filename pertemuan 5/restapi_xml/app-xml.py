from flask import Flask
import xml.dom.minidom as minidom

app = Flask(__name__)
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def main():
    # gunakan fungsi parse() untuk me-load xml ke memori
    # dan melakukan parsing
    doc = minidom.parse("mahasiswa.xml")

    # Cetak isi doc dan tag pertamanya
    print(doc.nodeName)
    print(doc.firstChild.tagName)

    nama = doc.getElementsByTagName("nama")[0].firstChild.data
    alamat = doc.getElementsByTagName("alamat")[0].firstChild.data
    jurusan = doc.getElementsByTagName("jurusan")[0].firstChild.data
    list_hobi = doc.getElementsByTagName("hobi")

    print("Nama: {}\nAlamat: {}\nJurusan: {}\n".format(nama, alamat, jurusan))

    print("Memiliki {} hobi:".format(len(list_hobi)))

    for hobi in list_hobi:
        print(" -", hobi.getAttribute("name"))

if __name__ == "main":
    main();
