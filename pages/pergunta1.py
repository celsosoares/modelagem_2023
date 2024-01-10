import streamlit as st
import pymysql

st.title('Pergunta 1')

st.subheader('Qual é o total de despesas por programa ao longo do período escolhido pelo usuário em um local determinado?')

def consultar_despesas_por_programa():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    # consulta_sql = f"""
    # SELECT p.descricao AS programa, SUM(d.valorAtualizado) AS total_despesas
    # FROM despesa d
    # INNER JOIN programa p ON d.projetoAtividade_id = p.id
    # WHERE d.data_despesa BETWEEN 'data_inicio' AND 'data_fim'
    # AND d.local = 'local_determinado'
    # GROUP BY p.descricao;
    # """

    consulta_sql = f"""
    SELECT p.descricao AS programa, SUM(d.valorAtualizado) AS total_despesas
    FROM despesa d
    INNER JOIN programa p ON d.projetoAtividade_id = p.id
    GROUP BY p.descricao;
    """

    try:
        cursor.execute(consulta_sql)
        resultados = cursor.fetchall()
        connection.close()

        return resultados

    except pymysql.Error as e:
        connection.close()
        raise e


# Main
try:
    resultados = consultar_despesas_por_programa()

    # if resultados:
    #     st.write("Total de despesas por programa:")
    #     for resultado in resultados:
    #         st.write(f"Programa: {resultado[0]}, Total de Despesas: {resultado[1]}")
    # else:
    #     st.write("Nenhum resultado encontrado para o período e local especificados.")

    st.write(resultados)

except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")
