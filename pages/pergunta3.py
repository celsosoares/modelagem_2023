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

    titulos = ["Local",
               "Descrição do Projeto ou Atividade",
               "Data",
               "Gasto Médio (R$)"]
    
    df_titulos = pd.DataFrame([titulos])
    df = pd.concat([df_titulos, df], ignore_index=True)

    st.table(df)

def consultar_locais():
    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E',
        port=57386,
        db='railway'
    )
    cursor = connection.cursor()
    consulta_sql = "SELECT DISTINCT bairro FROM dimorgao;"
    cursor.execute(consulta_sql)
    locais = [local[0] for local in cursor.fetchall()]
    connection.close()
    return locais

def consultar_projetos_atividades(local, data_inicial, data_final):
    connection = pymysql.connect(
        host='viaduct.proxy.rlwy.net',
        user='root',
        password='24c3b-bDbCdAC4aAh3A6GFEc12AAFg-E',
        port=57386,
        db='railway'
    )
    cursor = connection.cursor()

    consulta_sql = f"""
    SELECT do.bairro, dpa.descricao, di.data_id, AVG(fd.valorAtualizado) AS gasto_medio
    FROM fatodespesa fd
    JOIN dimorgao do ON fd.orgao_id = do.id
    JOIN dimprojetoatividade dpa ON fd.projetoAtividade_id = dpa.id
    JOIN dimdata di ON fd.dimdata_inicial_keyData = di.keyData
    WHERE do.bairro = '{local}' AND di.data_id >= '{data_inicial}' AND di.data_id <= '{data_final}'
    GROUP BY do.bairro, dpa.descricao, di.data_id
    ORDER BY gasto_medio DESC;
    """

    cursor.execute(consulta_sql)
    resultados = cursor.fetchall()
    connection.close()

    return resultados

locais = consultar_locais()
local = st.selectbox("Selecione o local", options=locais)

if local:
    data_inicial = st.date_input("Selecione a data inicial", value=pd.to_datetime('2022-01-01'))
    data_final = st.date_input("Selecione a data final", value=pd.to_datetime('2022-12-31'))

    try:
        resultados = consultar_projetos_atividades(local, data_inicial, data_final)
        exibir_resultados(resultados)
    except Exception as e:
        st.error(f"Ocorreu um erro na consulta: {e}")
