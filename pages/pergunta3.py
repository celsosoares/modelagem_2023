import streamlit as st
import pandas as pd
import pymysql

st.title('Pergunta 3')

st.subheader('Qual foi o gasto médio por projeto ou atividade em um período específico determinado pelo usuário em um local determinado?')

def exibir_resultados(resultados):
    if not resultados:
        st.write("Nenhum resultado encontrado.")
        return

    df = pd.DataFrame(resultados)

    titulos = ["Nome do Órgão",
               "Projeto Atividade",
               "Data",
               "Gasto Medio (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_gasto_medio():
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
        pa.descricao AS projeto_atividade_descricao,
        d.data_id AS periodo_selecionado,
        AVG(fd.valorAtualizado) AS gasto_medio
    FROM
        fatoDespesa fd
    JOIN
        dimOrgao o ON fd.orgao_id = o.id
    JOIN
        dimProjetoAtividade pa ON fd.projetoAtividade_id = pa.id
    JOIN
        dimData d ON fd.dimData_inicial_keyData = d.keyData
    WHERE
        d.data_id >= '2022-01-01' AND d.data_id <= '2022-12-31'
        AND o.descricao = 'Fundo Municipal de Desenvolvimento Social'
    GROUP BY
        o.descricao,
        pa.descricao,
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
    resultados = consultar_gasto_medio()
    exibir_resultados(resultados)
except Exception as e:
    st.error(f"Ocorreu um erro na consulta: {e}")