import streamlit as st
import pymysql

st.title('Pergunta 2')

st.subheader('Quais são as principais fontes de despesa em um determinado órgão durante o ano escolhido pelo usuário em um local determinado?')

def consultar_fontes_de_despesa_por_orgao():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    # consulta_sql = f"""
    # SELECT d.fonte_id, SUM(d.valorAtualizado) AS total_despesas_fonte
    # FROM despesa d
    # WHERE d.ano = 'ano_escolhido'
    # AND d.local = 'local_determinado'
    # AND d.orgao_id = 'id_orgao_escolhido'
    # GROUP BY d.fonte_id
    # ORDER BY total_despesas_fonte DESC;
    # """

    consulta_sql = f"""
    SELECT d.fonte_id, SUM(d.valorAtualizado) AS total_despesas_fonte
    FROM despesa d
    GROUP BY d.fonte_id
    ORDER BY total_despesas_fonte DESC;
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
    resultados = consultar_fontes_de_despesa_por_orgao()

    # if resultados:
    #     st.write("Total de despesas por programa:")
    #     for resultado in resultados:
    #         st.write(f"Programa: {resultado[0]}, Total de Despesas: {resultado[1]}")
    # else:
    #     st.write("Nenhum resultado encontrado para o período e local especificados.")

    st.write(resultados)

except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")