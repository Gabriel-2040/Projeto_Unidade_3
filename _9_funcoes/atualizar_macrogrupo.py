# database/operations.py
def atualizar_macrogrupo(conexao, cursor, padroes, macrogrupo_id):
    """Atualiza produtos com base nos padrões"""
    try:
        query = """
        UPDATE datawarehouse.dim_produtos
        SET macrogrupo_id = %s
        WHERE prod_und ILIKE ANY(ARRAY[%s])
        """
        cursor.execute(query, (macrogrupo_id, padroes))
        print(f"✓ Macrogrupo {macrogrupo_id}: {cursor.rowcount} registros atualizados")
        return True
        
    except psycopg2.Error as e:
        print(f"✗ Erro ao atualizar macrogrupo {macrogrupo_id}: {e}")
        return False