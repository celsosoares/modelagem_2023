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

    titulos = ["Nome do Órgão", "Descrição do Programa", "Bairro", "Data", "Total de Despesas (R$)"]
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)
    st.table(df)

def consultar_orgaos():
    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net', user='root',port=57386 ,password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E', db='railway')
    cursor = connection.cursor()
    consulta_sql = "SELECT descricao FROM dimorgao;"
    cursor.execute(consulta_sql)
    orgaos = [orgao[0] for orgao in cursor.fetchall()]
    connection.close()
    return orgaos

def consultar_programas(orgao):
    if orgao is None:
        return ["None"]

    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net', user='root',port=57386 ,password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E', db='railway')
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT DISTINCT dp.descricao
    FROM dimorgao do
    JOIN fatodespesa fd ON do.id = fd.orgao_id
    JOIN dimprograma dp ON fd.programa_id = dp.id
    WHERE do.descricao = '{orgao}';
    """
    
    cursor.execute(consulta_sql)
    programas = [programa[0] for programa in cursor.fetchall()]
    
    connection.close()

    return programas

def consultar_bairros(orgao):
    if orgao is None:
        return ["None"]

    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net', user='root',port=57386 ,password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E', db='railway')
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT DISTINCT bairro FROM dimorgao 
    WHERE descricao = '{orgao}';
    """
    
    cursor.execute(consulta_sql)
    bairros = ["None"] + [bairro[0] for bairro in cursor.fetchall()]
    
    connection.close()

    return bairros

def consultar_despesas_por_programa(data_inicial, data_final, orgao, programa, bairro):
    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net', user='root',port=57386 ,password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E', db='railway')
    cursor = connection.cursor()

    where_clause = f"di.data_id >= '{data_inicial}' AND di.data_id <= '{data_final}'"

    if orgao and orgao != "None":
        where_clause += f" AND o.descricao = '{orgao}'"
    if programa and programa != "None":
        where_clause += f" AND p.descricao = '{programa}'"
    if bairro and bairro != "None":
        where_clause += f" AND o.bairro = '{bairro}'"

    consulta_sql = f"""
    SELECT
        o.descricao AS orgao_descricao,
        p.descricao AS programa_descricao,
        o.bairro AS bairro,
        di.data_id AS periodo_pesquisado,
        SUM(fd.valorAtualizado) AS total_despesas
    FROM
        fatodespesa fd
    JOIN
        dimorgao o ON fd.orgao_id = o.id
    JOIN
        dimprograma p ON fd.programa_id = p.id
    JOIN
        dimdata di ON fd.dimData_inicial_keyData = di.keyData
    WHERE
        {where_clause}
    GROUP BY
        o.descricao,
        p.descricao,
        o.bairro,
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

orgaos = consultar_orgaos()
orgao = st.selectbox("Selecione o órgão", options=["None"] + orgaos)

if orgao != "None":
    programas = consultar_programas(orgao)
    programa = st.selectbox("Selecione o programa", options=programas)

    bairros = consultar_bairros(orgao)
    bairro = st.selectbox("Selecione o bairro", options=bairros)

    data_inicial = st.date_input("Selecione a data inicial", value=pd.to_datetime('2022-01-01'))
    data_final = st.date_input("Selecione a data final", value=pd.to_datetime('2022-12-31'))

    try:
        resultados = consultar_despesas_por_programa(data_inicial, data_final, orgao, programa, bairro)
        exibir_resultados(resultados)
    except Exception as e:
        st.error(f"Ocorreu um erro na consulta: {e}")
