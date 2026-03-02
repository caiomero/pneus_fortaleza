import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

# =========================
# CONEXÃO COM POSTGRESQL
# =========================

def get_connection():
    return psycopg2.connect(os.environ["DATABASE_URL"])

# =========================
# CRIAR TABELAS
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
            valor NUMERIC
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

# =========================
# LISTAR + BUSCAR CLIENTES
# =========================

@app.route("/clientes")
def clientes():
    busca = request.args.get("busca")

    conn = get_connection()
    cursor = conn.cursor()

    if busca:
        cursor.execute(
            "SELECT * FROM clientes WHERE nome ILIKE %s ORDER BY id DESC",
            (f"%{busca}%",)
        )
    else:
        cursor.execute("SELECT * FROM clientes ORDER BY id DESC")

    dados = cursor.fetchall()
    conn.close()

    return render_template("clientes.html", clientes=dados)

# =========================
# ADICIONAR CLIENTE
# =========================

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
    conn.close()

    return redirect("/clientes")

# =========================
# DELETAR CLIENTE
# =========================

@app.route("/delete/<int:id>")
def delete_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM clientes WHERE id = %s", (id,))

    conn.commit()
    conn.close()

    return redirect("/clientes")

# =========================
# EDITAR CLIENTE
# =========================

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar_cliente(id):
    conn = get_connection()
    cursor = conn.cursor()

    if request.method == "POST":
        nome = request.form["nome"]
        telefone = request.form["telefone"]
        veiculo = request.form["veiculo"]
        placa = request.form["placa"]
        descricao = request.form["descricao"]

        cursor.execute("""
            UPDATE clientes
            SET nome=%s, telefone=%s, veiculo=%s, placa=%s, descricao=%s
            WHERE id=%s
        """, (nome, telefone, veiculo, placa, descricao, id))

        conn.commit()
        conn.close()
        return redirect("/clientes")

    cursor.execute("SELECT * FROM clientes WHERE id=%s", (id,))
    cliente = cursor.fetchone()
    conn.close()

    return render_template("editar.html", cliente=cliente)

# =========================
# SERVIÇOS
# =========================

@app.route("/servicos")
def servicos():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM servicos ORDER BY id DESC")
    dados = cursor.fetchall()

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
    conn.close()

    return redirect("/servicos")

# =========================
# EXECUÇÃO
# =========================

if __name__ == "__main__":
    app.run(debug=True)
