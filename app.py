from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Criar banco se não existir
def init_db():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            veiculo TEXT,
            placa TEXT
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route("/")
def index():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=clientes)

@app.route("/add", methods=["POST"])
def add_cliente():
    nome = request.form["nome"]
    telefone = request.form["telefone"]
    veiculo = request.form["veiculo"]
    placa = request.form["placa"]

    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clientes (nome, telefone, veiculo, placa) VALUES (?, ?, ?, ?)",
                   (nome, telefone, veiculo, placa))
    conn.commit()
    conn.close()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete_cliente(id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
