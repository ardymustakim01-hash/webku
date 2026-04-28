from flask import Flask, render_template, request, redirect
import os

app = Flask(__name__)

DATA_FILE = "data.txt"

# Fungsi baca data dari file
def load_data():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return f.read().splitlines()

# Fungsi simpan data ke file
def save_data(data):
    with open(DATA_FILE, "w") as f:
        f.write("\n".join(data))

# Halaman utama
@app.route("/", methods=["GET", "POST"])
def index():
    data = load_data()

    if request.method == "POST":
        nama = request.form["nama"]
        if nama:
            data.append(nama)
            save_data(data)
        return redirect("/")

    return render_template("index.html", data=data)

# Hapus data
@app.route("/delete/<int:index>")
def delete(index):
    data = load_data()
    if 0 <= index < len(data):
        data.pop(index)
        save_data(data)
    return redirect("/")

# Edit data
@app.route("/edit/<int:index>", methods=["GET", "POST"])
def edit(index):
    data = load_data()

    if request.method == "POST":
        data[index] = request.form["nama"]
        save_data(data)
        return redirect("/")

    return render_template("edit.html", index=index, nama=data[index])

# Run app (untuk deploy)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)