# database/connection.py
import psycopg2

def conectar_banco():
    """Estabelece conexão com o banco de dados"""
    try:
        conexao = psycopg2.connect(
                host="localhost",
                port=5433,
                database="projeto_python_da18",
                user="postgres",
                password="1234",
                connect_timeout=5

        )
        cursor = conexao.cursor()
        print("✓ Conexão estabelecida com sucesso")
        return conexao, cursor
        
    except psycopg2.Error as e:
        print(f"✗ Erro ao conectar: {e}")
        return None, None