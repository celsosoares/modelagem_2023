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
               "Descrição da Fonte",
               "Bairro",
               "Ano",
               "Total de Despesas (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_orgaos():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()
    consulta_sql = "SELECT descricao FROM dimOrgao;"
    cursor.execute(consulta_sql)
    orgaos = [orgao[0] for orgao in cursor.fetchall()]
    connection.close()
    return orgaos

def consultar_fontes(orgao, ano):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT do.descricao AS orgao_descricao, df.descricao AS fonte_descricao, do.bairro AS bairro,
           EXTRACT(YEAR FROM di.data_id) AS ano, SUM(fd.valorAtualizado) AS total_despesas
    FROM fatoDespesa fd
    JOIN dimOrgao do ON fd.orgao_id = do.id
    JOIN dimFonte df ON fd.fonte_id = df.id
    JOIN dimData di ON fd.dimData_inicial_keyData = di.keyData
    WHERE do.descricao = '{orgao}' AND EXTRACT(YEAR FROM di.data_id) = {ano}
    GROUP BY orgao_descricao, fonte_descricao, bairro, ano
    ORDER BY total_despesas DESC;
    """

    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()
    connection.close()

    return resultados

orgaos = consultar_orgaos()
orgao = st.selectbox("Selecione o órgão", options=orgaos)

if orgao:
    ano = st.number_input("Digite o ano:", min_value=2000, max_value=2100)

    try:
        resultados = consultar_fontes(orgao, ano)
        exibir_resultados(resultados)
    except Exception as e:
        st.error(f"Ocorreu um erro na consulta: {e}")
