#importar librerias
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pycaret.clustering import create_model, assign_model, setup

st.sidebar.image('SmartBI.png')
st.subheader('Agrupación de pozos con características geográficas similares')

# Cargando datos iniciales
st.subheader('Datos originales')
coordenadas_pozo_df = pd.read_excel("coordenadas_pozo_rs.xlsx")
st.write(coordenadas_pozo_df)

# Entrenando el modelo
st.subheader('Un momento, entrenando el modelo')
cl = setup(data=coordenadas_pozo_df)
modelo = create_model('kmeans', num_clusters = 4)

# Colores de los grupos
colores = ["royalblue","crimson","lightseagreen","orange"]


def main():
   
    st.subheader('Agrupar pozos')
    st.write('Este proceso puede llevar unos segundos')
        
    if st.button('AGRUPAR'):
                
        st.subheader('Datos Agrupados')
      
        dataset = assign_model(modelo)
        st.write(dataset)
        
        asignar = []
        for index, row in dataset.iterrows():
            if(row['Cluster'] == 'Cluster 0'):
                asignar.append(colores[0])
                
            elif(row['Cluster'] == 'Cluster 1'):
                asignar.append(colores[1])
                    
            elif(row['Cluster'] == 'Cluster 2'):
                asignar.append(colores[2])
                        
            else:
                asignar.append(colores[3])
        
        fig = go.Figure(data=go.Scattergeo(
            lon = dataset['Longitude'],
            lat = dataset['Latitude'],
            text = dataset['Pozo'],   
            marker = dict(
                color = asignar)
            ))    
    
        fig.update_layout(
            geo_scope ='north america',)
    
        st.plotly_chart(fig)
    
if __name__ == '__main__':
    main()
    