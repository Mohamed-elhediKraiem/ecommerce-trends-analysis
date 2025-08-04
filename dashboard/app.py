import pandas as pd
import streamlit as st
import plotly.express as px

st.title("📈 Évolution des commandes par année")
df = pd.read_csv('../data/Sample - Superstore.csv', encoding='latin1')

# Filtrage par pays
pays = st.selectbox("Choisissez un pays", df['Country'].unique())
df = df[df['Country'] == pays]

# Extraction de l'année
df['Order Date'] = pd.to_datetime(df['Order Date'])
df['year'] = df['Order Date'].dt.year

# Nombre de commandes par année
commandes_par_annee = df.groupby('year').size()

# 📈 Graphique Plotly
fig = px.line(x=commandes_par_annee.index,
              y=commandes_par_annee.values,
              labels={'x': 'Année', 'y': 'Nombre de commandes'},
              title=f"Évolution des commandes - {pays}")

st.plotly_chart(fig)

# 💰 Graphique des ventes
ventes_par_annee = df.groupby('year')['Sales'].sum()

fig2 = px.line(x=ventes_par_annee.index,
               y=ventes_par_annee.values,
               labels={'x': 'Année', 'y': 'Montant des ventes (€)'},
               title=f"Évolution des ventes - {pays}")

st.plotly_chart(fig2)
