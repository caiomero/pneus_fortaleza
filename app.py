import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# =========================
# CONEXÃO COM BANCO (POSTGRES RENDER)
# =========================

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    return psycopg2.connect(DATABASE_URL)

# =========================
# CRIAR TABELAS (SE NÃO EXISTIREM)
# =========================

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id SERIAL PRIMARY KEY,
            nome TEXT NOT NULL,
            telefone TEXT,
            veiculo TEXT,
            placa TEXT,
            descricao TEXT
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS servicos (
            id SERIAL PRIMARY KEY,
            cliente TEXT,
            descricao TEXT,
            valor REAL
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()

# Chama a função depois de definir ela
init_db()

# =========================
# ROTAS
# =========================

@app.route("/")
def home():
    return redirect("/clientes")

@app.route("/clientes")
def clientes():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clientes.html", clientes=dados)

@app.route("/add_cliente", methods=["POST"])
def add_cliente():
    nome = request.form["nome"]
    telefone = request.form.get("telefone")
    veiculo = request.form.get("veiculo")
    placa = request.form.get("placa")
    descricao = request.form.get("descricao")

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO clientes (nome, telefone, veiculo, placa, descricao)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, telefone, veiculo, placa, descricao))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/clientes")

@app.route("/delete/<int:id>")
def delete_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    return redirect("/clientes")

@app.route("/servicos")
def servicos():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM servicos ORDER BY id DESC")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("servicos.html", servicos=dados)

@app.route("/add_servico", methods=["POST"])
def add_servico():
    cliente = request.form["cliente"]
    descricao = request.form["descricao"]
    valor = request.form["valor"]

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO servicos (cliente, descricao, valor)
        VALUES (%s, %s, %s)
    """, (cliente, descricao, valor))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect("/servicos")

# =========================
# EXECUÇÃO LOCAL
# =========================

if __name__ == "__main__":
    app.run(debug=True)
