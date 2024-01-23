import streamlit as st
import pandas as pd
import pymysql

st.title('Pergunta 1')

st.subheader('Qual é o total de despesas por programa ao longo do período escolhido pelo usuário em um local determinado?')

def exibir_resultados(resultados):
    if not resultados:
        st.write("Nenhum resultado encontrado.")
        return

    df = pd.DataFrame(resultados)

    titulos = ["Nome do Órgão",
               "Descrição do Programa",
               "Data",
               "Total de Despesas (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_despesas_por_programa():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT
        o.descricao AS orgao_descricao,
        p.descricao AS programa_descricao,
        di.data_id AS periodo_pesquisado,
        SUM(fd.valorAtualizado) AS total_despesas
    FROM
        fatoDespesa fd
    JOIN
        dimOrgao o ON fd.orgao_id = o.id
    JOIN
        dimPrograma p ON fd.programa_id = p.id
    JOIN
        dimData di ON fd.dimData_inicial_keyData = di.keyData
    WHERE
        di.data_id >= '2022-01-01' AND di.data_id <= '2022-12-31'
        AND o.descricao = 'Fundo Municipal de Desenvolvimento Social'
    GROUP BY
        o.descricao,
        p.descricao,
        di.data_id;
    """

    try:
        cursor.execute(consulta_sql)
        resultados = cursor.fetchall()
        connection.close()

        return resultados

    except pymysql.Error as e:
        connection.close()
        raise e


try:
    resultados = consultar_despesas_por_programa()
    exibir_resultados(resultados)
except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")
