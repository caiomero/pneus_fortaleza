import os
import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    try:
        return psycopg2.connect(DATABASE_URL)
    except Exception as e:
        print("Erro ao conectar no banco:", e)
        return None

@app.before_first_request
def init_db():
    conn = get_connection()
    if not conn:
        print("Banco não conectado.")
        return

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

@app.route("/")
def home():
    return redirect("/clientes")

@app.route("/clientes")
def clientes():
    conn = get_connection()
    if not conn:
        return "Erro ao conectar no banco."

    cursor = conn.cursor()
    cursor.execute("SELECT * FROM clientes ORDER BY id DESC")
    dados = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template("clientes.html", clientes=dados)

if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
    
    

