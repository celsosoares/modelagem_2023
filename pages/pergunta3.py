import streamlit as st
import pymysql

st.title('Pergunta 3')

st.subheader('Qual foi o gasto médio por projeto ou atividade em um período específico determinado pelo usuário em um local determinado?')

def consultar_gasto_medio():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    # consulta_sql = f"""
    # SELECT d.projetoAtividade_id, AVG(d.valorAtualizado) AS gasto_medio
    # FROM despesa d
    # WHERE d.data_despesa BETWEEN 'data_inicio' AND 'data_fim'
    # AND d.local = 'local_determinado'
    # GROUP BY d.projetoAtividade_id;
    # """

    consulta_sql = f"""
    SELECT d.projetoAtividade_id, AVG(d.valorAtualizado) AS gasto_medio
    FROM despesa d
    GROUP BY d.projetoAtividade_id;
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
    resultados = consultar_gasto_medio()

    # if resultados:
    #     st.write("Total de despesas por programa:")
    #     for resultado in resultados:
    #         st.write(f"Programa: {resultado[0]}, Total de Despesas: {resultado[1]}")
    # else:
    #     st.write("Nenhum resultado encontrado para o período e local especificados.")

    st.write(resultados)

except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")