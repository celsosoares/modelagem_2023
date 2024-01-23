import streamlit as st
import pandas as pd

import pymysql

st.title('Pergunta 2')

st.subheader('Quais são as principais fontes de despesa em um determinado órgão durante o ano escolhido pelo usuário em um local determinado?')

def exibir_resultados(resultados):
    if not resultados:
        st.write("Nenhum resultado encontrado.")
        return

    df = pd.DataFrame(resultados)

    titulos = ["Nome do Órgão",
               "Fonte",
               "Data",
               "Total de Despesas (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_fontes_de_despesa_por_orgao():
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
        f.descricao AS fonte_descricao,
        d.ano_nome AS periodo_selecionado,
        SUM(fd.valorAtualizado) AS total_despesas
    FROM
        fatoDespesa fd
    JOIN
        dimOrgao o ON fd.orgao_id = o.id
    JOIN
        dimFonte f ON fd.fonte_id = f.id
    JOIN
        dimData d ON fd.dimData_inicial_keyData = d.keyData
    WHERE
        d.ano_nome = '2023'
        AND o.descricao = 'Fundo Municipal de Desenvolvimento Social'
    GROUP BY
        o.descricao,
        f.descricao,
        d.ano_nome;
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
    exibir_resultados(resultados)
except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")