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
               "Bairro",
               "Data",
               "Total de Despesas (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_locais():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()
    consulta_sql = "SELECT DISTINCT bairro FROM dimOrgao;"
    cursor.execute(consulta_sql)
    locais = [local[0] for local in cursor.fetchall()]
    connection.close()
    return locais

def consultar_subfuncoes():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()
    consulta_sql = "SELECT DISTINCT descricaoSubFunc FROM dimSubFuncao;"
    cursor.execute(consulta_sql)
    subfuncoes = [subfuncao[0] for subfuncao in cursor.fetchall()]
    connection.close()
    return subfuncoes

def consultar_orgaos(local):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()
    consulta_sql = f"SELECT DISTINCT descricao FROM dimOrgao WHERE bairro = '{local}';"
    cursor.execute(consulta_sql)
    orgaos = [orgao[0] for orgao in cursor.fetchall()]
    connection.close()
    return orgaos

def consultar_despesas(orgao, subfuncao, local, data_inicial, data_final):
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='root',
        db='dw_exec_orcamentaria_sp'
    )
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT do.descricao AS orgao_descricao, dsf.descricaoSubFunc, do.bairro AS bairro, di.data_id, SUM(fd.valorAtualizado) AS total_despesas
    FROM fatoDespesa fd
    JOIN dimOrgao do ON fd.orgao_id = do.id
    JOIN dimSubFuncao dsf ON fd.subFuncao_id = dsf.id
    JOIN dimData di ON fd.dimData_inicial_keyData = di.keyData
    WHERE do.descricao = '{orgao}' AND dsf.descricaoSubFunc = '{subfuncao}'
    AND do.bairro = '{local}' AND di.data_id >= '{data_inicial}' AND di.data_id <= '{data_final}'
    GROUP BY do.descricao, dsf.descricaoSubFunc, do.bairro, di.data_id
    ORDER BY total_despesas DESC;
    """

    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()
    connection.close()

    return resultados

locais = consultar_locais()
local = st.selectbox("Selecione o local", options=locais)

subfuncoes = consultar_subfuncoes()
subfuncao = st.selectbox("Selecione a subfunção", options=subfuncoes)

if local and subfuncao:
    orgaos = consultar_orgaos(local)
    orgao = st.selectbox("Selecione o órgão", options=orgaos)

    if orgao:
        data_inicial = st.date_input("Selecione a data inicial", value=pd.to_datetime('2022-01-01'))
        data_final = st.date_input("Selecione a data final", value=pd.to_datetime('2022-12-31'))

        try:
            resultados = consultar_despesas(orgao, subfuncao, local, data_inicial, data_final)
            exibir_resultados(resultados)
        except Exception as e:
            st.error(f"Ocorreu um erro na consulta: {e}")
