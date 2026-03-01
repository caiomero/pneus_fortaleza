import os
import sqlite3
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# =========================
# BANCO DE DADOS
# =========================

def init_db():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Tabela clientes
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT,
            veiculo TEXT,
            placa TEXT,
            descricao TEXT
        )
    """)

    # Tabela serviços
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            descricao TEXT,
            valor REAL
        )
    """)

    conn.commit()
    conn.close()

init_db()

# =========================
# ROTAS
# =========================

@app.route("/")
def home():
    return redirect("/clientes")

@app.route("/clientes")
def clientes():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=dados)

@app.route("/add_cliente", methods=["POST"])
def add_cliente():
    nome = request.form["nome"]
    telefone = request.form.get("telefone")
    veiculo = request.form.get("veiculo")
    placa = request.form.get("placa")
    descricao = request.form.get("descricao")

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nome, telefone, veiculo, placa, descricao)
        VALUES (?, ?, ?, ?, ?)
    """, (nome, telefone, veiculo, placa, descricao))

    conn.commit()
    conn.close()

    return redirect("/clientes")

@app.route("/delete/<int:id>")
def delete_cliente(id):
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect("/clientes")

@app.route("/servicos")
def servicos():
    return render_template("servicos.html")

@app.route("/add_servico", methods=["POST"])
def add_servico():
    cliente = request.form["cliente"]
    descricao = request.form["descricao"]
    valor = request.form["valor"]

    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO servicos (cliente, descricao, valor)
        VALUES (?, ?, ?)
    """, (cliente, descricao, valor))

    conn.commit()
    conn.close()

    return redirect("/servicos")

# =========================
# EXECUÇÃO LOCAL
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
