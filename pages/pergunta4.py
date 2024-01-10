import streamlit as st
import pymysql

st.title('Pergunta 4')

st.subheader('Quais órgãos gastaram mais em uma subfunção específica em um período e local determinado?')

def consultar_gastos_por_orgao():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    # consulta_sql = f"""
    # SELECT o.descricao AS orgao, SUM(d.valorAtualizado) AS total_despesas
    # FROM despesa d
    # JOIN orgao o ON d.orgao_id = o.id
    # WHERE d.data_despesa BETWEEN 'data_inicio' AND 'data_fim'
    # AND d.local = 'local_determinado'
    # AND d.subFuncao_id = 'id_subfuncao_especifica'
    # GROUP BY o.descricao
    # ORDER BY total_despesas DESC;
    # """

    consulta_sql = f"""
    SELECT o.descricao AS orgao, SUM(d.valorAtualizado) AS total_despesas
    FROM despesa d
    JOIN orgao o ON d.orgao_id = o.id
    GROUP BY o.descricao
    ORDER BY total_despesas DESC;
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
    resultados = consultar_gastos_por_orgao()

    # if resultados:
    #     st.write("Total de despesas por programa:")
    #     for resultado in resultados:
    #         st.write(f"Programa: {resultado[0]}, Total de Despesas: {resultado[1]}")
    # else:
    #     st.write("Nenhum resultado encontrado para o período e local especificados.")

    st.write(resultados)

except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")