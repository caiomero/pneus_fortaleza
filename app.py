from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# =========================
# CRIAR BANCO
# =========================
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

# =========================
# DASHBOARD
# =========================
@app.route("/")
def index():
    return redirect("/clientes")
# =========================
# CLIENTES
# =========================
@app.route("/clientes")
def clientes():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=dados)

# =========================
# ADICIONAR CLIENTE
# =========================
@app.route("/add_cliente", methods=["POST"])
def add_cliente():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, telefone, veiculo, placa)
        VALUES (?, ?, ?, ?)
    """, (
        request.form["nome"],
        request.form["telefone"],
        request.form["veiculo"],
        request.form["placa"]
    ))
    conn.commit()
    conn.close()
    return redirect("/clientes")

# =========================
# EXCLUIR CLIENTE
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/clientes")

# =========================
# RENDER
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

