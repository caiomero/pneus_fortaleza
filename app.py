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

# 🔥 SOLUÇÃO RÁPIDA:
# Página inicial redireciona para /clientes
@app.route("/")
def index():
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
        CREATE TABLE IF NOT EXISTS servicos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            descricao TEXT,
            valor REAL
        )
    """)

    cursor.execute("INSERT INTO servicos (cliente, descricao, valor) VALUES (?, ?, ?)",
                   (cliente, descricao, valor))

    conn.commit()
    conn.close()

    return redirect("/servicos")
    
@app.route("/clientes")
def clientes():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes")
    dados = cursor.fetchall()
    conn.close()
    return render_template("clientes.html", clientes=dados)

@app.route("/add_cliente", methods=["POST"])
def add_cliente():
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO clientes (nome, telefone, veiculo, placa)
        VALUES (?, ?, ?, ?)
    """, (
        request.form.get("nome"),
        request.form.get("telefone"),
        request.form.get("veiculo"),
        request.form.get("placa")
    ))
    conn.commit()
    conn.close()
    return redirect("/clientes")

@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect("clientes.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/clientes")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

