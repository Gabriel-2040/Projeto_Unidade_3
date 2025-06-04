# database/close.py
def fechar_conexao(conexao, cursor):
    """Encerra a conexão com o banco"""
    try:
        if conexao:
            conexao.commit()
            cursor.close()
            conexao.close()
            print("✓ Conexão encerrada com sucesso")
    except psycopg2.Error as e:
        print(f"✗ Erro ao fechar conexão: {e}")