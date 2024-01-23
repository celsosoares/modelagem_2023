import streamlit as st
import pandas as pd

import pymysql

st.title('Pergunta 4')

st.subheader('Quais órgãos gastaram mais em uma subfunção específica em um período e local determinado?')

def exibir_resultados(resultados):
    if not resultados:
        st.write("Nenhum resultado encontrado.")
        return

    df = pd.DataFrame(resultados)

    titulos = ["Nome do Órgão",
               "Subfunção",
               "Data",
               "Total de Despesas (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_gastos_por_orgao():
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
        sf.descricaoSubFunc AS subfuncao_descricao,
        d.data_id AS periodo_selecionado,
        SUM(fd.valorAtualizado) AS total_despesas
    FROM
        fatoDespesa fd
    JOIN
        dimOrgao o ON fd.orgao_id = o.id
    JOIN
        dimSubFuncao sf ON fd.subFuncao_id = sf.id
    JOIN
        dimData d ON fd.dimData_inicial_keyData = d.keyData
    WHERE
        d.data_id >= '2022-01-01' AND d.data_id <= '2022-12-31'
        AND o.descricao = 'Fundo Municipal de Desenvolvimento Social'
        AND sf.descricaoSubFunc = 'Ensino Fundamental'
    GROUP BY
        o.descricao,
        sf.descricaoSubFunc,
        d.data_id;
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
    exibir_resultados(resultados)
except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")