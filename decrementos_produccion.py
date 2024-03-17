#importar librerias
import streamlit as st
import pandas as pd
import plotly.express as px
from pycaret.clustering import create_model, assign_model, setup

st.sidebar.image('SmartBI.png')
st.subheader('Agrupación de pozos con decrementos de produccion')

# Cargando datos iniciales
st.subheader('Datos originales')
df = pd.read_csv(r"decrementos_produccion.csv")

# disminuir el número de registros, ya que streamlit cloud solo acepta 1 GB
df = df.head(25000)

#df= df[df['FECHA'] == '01/05/2018']

st.write(df)
fig = px.scatter(df, x="FECHA", y="ACEITE", hover_data = {"UWI"})
st.write(fig)
#fig.show()
       
# Entrenando el modelo
st.subheader('Un momento, entrenando el modelo')
cl = setup(data=df)
modelo = create_model('kmeans', num_clusters = 3)

def main():
   
    st.subheader('Agrupar pozos')
    st.write('Este proceso puede llevar unos segundos')
        
    if st.button('AGRUPAR'):
                
        st.subheader('Datos Agrupados')
      
        dataset = assign_model(modelo)
        st.write(dataset)
        fig = px.scatter(dataset, x="FECHA", y="ACEITE", hover_data = {"UWI"}, color='Cluster',
                         color_discrete_map={'Cluster 0':'green','Cluster 1':'orange','Cluster 2':'blue'})
        st.write(fig)
        
        st.subheader('Cluster 0')
        dataset1 = dataset[dataset['Cluster']=='Cluster 0']
        st.write(dataset1)
        fig = px.scatter(dataset1, x="FECHA", y="ACEITE", hover_data = {"UWI"}, color='Cluster',
                         color_discrete_map={'Cluster 0':'green'})
        st.write(fig)
        
        st.subheader('Cluster 1')
        dataset2 = dataset[dataset['Cluster']=='Cluster 1']
        st.write(dataset2)
        fig = px.scatter(dataset2, x="FECHA", y="ACEITE", hover_data = {"UWI"}, color='Cluster',
                         color_discrete_map={'Cluster 1':'orange'})
        st.write(fig)
        
        st.subheader('Cluster 2')
        dataset3 = dataset[dataset['Cluster']=='Cluster 2']
        st.write(dataset3)
        fig = px.scatter(dataset3, x="FECHA", y="ACEITE", hover_data = {"UWI"}, color='Cluster',
                         color_discrete_map={'Cluster 2':'blue'})
        st.write(fig)
        
           
if __name__ == '__main__':
    main()
    