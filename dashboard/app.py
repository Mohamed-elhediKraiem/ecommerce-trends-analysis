import pandas as pd
import streamlit as st
import plotly.express as px
import os
import pgeocode

st.title("📈 Évolution des commandes par année")
file_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'Sample - Superstore.csv')
df = pd.read_csv(file_path, encoding='latin1')

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

###############################################
#####################################MAP

postal_codes = df["Postal Code"].astype(str).tolist()
nomi = pgeocode.Nominatim('us')  # 'us' = United States
us_post = nomi.query_postal_code(postal_codes)

# Ajouter latitude et longitude dans ton DataFrame
df['latitude'] = us_post['latitude'].values
df['longitude'] = us_post['longitude'].values

df_geo = df.groupby(['City','latitude', 'longitude']).agg({
    'Sales': 'sum',
    'Postal Code': 'count'  # nombre de commandes par zone
}).rename(columns={'Postal Code': 'Nb_commandes'}).reset_index()

fig = px.scatter_mapbox(df_geo,
                        lat='latitude', lon='longitude',
                        size='Sales',
                        color='Sales',
                        hover_name='City',
                        mapbox_style="open-street-map",
                        zoom=3,
                        title="Carte des ventes par code postal")

st.plotly_chart(fig)