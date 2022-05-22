#!/usr/bin/env python
# coding: utf-8

# ##  Bibliotecas:

# In[6]:


import pandas as pd
import gspread
from google.oauth2 import service_account
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np 
import os
from PIL import Image


# ##  Integração com API do Google Sheets :

# In[7]:


# Arquivos de Autorização
scopes = ["https://www.googleapis.com/auth/spreadsheets",
          "https://www.googleapis.com/auth/drive"]
json_file = (r"C:\Users\breno\Desktop\TESTE_SRICPT\SCRIPT_STREAMLIT\chave_api.json")

#Função para Logar da API do Google Sheet
def login():
    credentials = service_account.Credentials.from_service_account_file(json_file)
    scoped_credentials = credentials.with_scopes(scopes)
    gc = gspread.authorize(scoped_credentials)
    return gc

#Abrir a planilha como DataFrame
nome="Planilha"
aba="satelite"

gc = login()
planilha = gc.open(nome)
aba = planilha.worksheet(aba)
dados = aba.get_all_records()
df = pd.DataFrame(dados)
df['Area'] = pd.to_numeric(df['Area'], errors='coerce')


# ##  Abrindo Planilha

# In[8]:


#Abrindo a tabela em csv 
tabela = df

#Tabela area total por Email
tabela_area_total = tabela.groupby(['E-mail'])['Area'].sum().reset_index()

#Tabela area total por Email e Fazenda
tabela_fazenda = tabela.groupby(['E-mail','Fazenda'])['Area'].sum().reset_index()


# ##  Dash Board

# In[9]:


#Barra Lateral
barra_lateral = st.sidebar.empty()
st.sidebar.markdown('## Dashboard:')
st.sidebar.markdown("- Visualização dos Dados de Satélite 🛰️")

#Selecionar E-mail
filtro_email = st.sidebar.selectbox('Selecione o E-mail:',(tabela_area_total['E-mail']))

#Dados por Email
dados = tabela['E-mail'] == filtro_email
st.markdown("# Dados do E-mail:")
filtrados = tabela[dados]
filtrados = filtrados.astype(str)
st.write(filtrados)
csv = filtrados.to_csv(sep=';')

#Download CSV
st.download_button(label="⬇️ Download CSV",data=csv,file_name='tabela.csv', mime='csv')

#Colunas 
col1, col2, col3 = st.columns(3)

#Area Total 
area = tabela_area_total['E-mail'] == filtro_email
area_filtrada = tabela_area_total[area]
area_total = area_filtrada['Area'].unique().astype(float)
col1.metric(label="☑️ Área Total (ha)", value= area_total)

# Número de Fazenda 
n_fazenda = filtrados.nunique()
n_fazenda = n_fazenda[1]
col2.metric(label="🧑‍🌾 N° Fazendas", value= n_fazenda)

#Número de Talhões 
n_talhoes = filtrados.nunique()
n_talhoes = n_talhoes[2]
col3.metric(label="🚜 N° Talhões", value= n_talhoes)


#Gráfico de Barras - Área por Fazenda 
fazenda = tabela_fazenda['E-mail'] == filtro_email
fazenda_filtrados = tabela_fazenda[fazenda]
st.title('Área por Fazenda:')
fig = px.bar(y = fazenda_filtrados['Fazenda'],x = fazenda_filtrados['Area'],labels={'y':'Fazenda','x':'Área (ha)'})
fig.update_layout(title={'text' : 'Requisições de Satélite por Fazenda', 'y': 0.9, 'x': 0.5},title_font_size=18)
st.plotly_chart(fig)


#Gráfico de Barras - Área por Talhão 
filtrados_t = filtrados.groupby(['E-mail','Fazenda'])['Area'].sum().reset_index()
st.title('Área por Talhão da Fazenda:')
filtro_fazenda = st.selectbox('Selecione a Fazenda:',(filtrados_t['Fazenda']))
talhao = filtrados['Fazenda'] == filtro_fazenda
talhao_filtrados = filtrados[talhao]
fig_talhao = px.bar(y = talhao_filtrados['Area'],x = talhao_filtrados['Talhão'], labels={'y':'Área (ha)','x':'Talhão'})
fig_talhao.update_layout(title={'text' : 'Requisições de Satélite por Talhão', 'y':0.9, 'x': 0.5},title_font_size=18)
st.plotly_chart(fig_talhao)


# In[ ]:





# In[ ]:




