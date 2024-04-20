#importar librerias
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px
from pycaret.regression import *


st.sidebar.image('SmartBI.png')

st.header('Predicción de Qo que habrá después de la estimulación')

# Cargando datos
te_df = pd.read_csv(r"tratamientos_estimulacion.csv")

st.subheader('Datos de entrada, para entrenar el modelo')
st.write(te_df)

st.subheader('Análisis Exploratorio de los Datos')

eje_x_seleccionado = st.selectbox("Variable que desea en el eje x", ["solvente","acido","quelante","divergente","Intervalo","Qo antes"])
eje_y_seleccionado = st.selectbox("Variable que desea en el eje y", ["solvente","acido","quelante","divergente","Intervalo","Qo antes"])

alt_char = (
    alt.Chart(te_df, title = "Grafico de Dispersión Tratamiento Estimulaciones")
    .mark_circle()
    .encode(
        x=eje_x_seleccionado,
        y=eje_y_seleccionado)
    .interactive()
    
    )

st.altair_chart(alt_char, use_container_width=True)

st.write(f'Histograma de {eje_x_seleccionado}')
fig = px.histogram(te_df[eje_x_seleccionado])
st.plotly_chart(fig, use_container_width=True)

# Cargando datos a predecir
te_df_pre = pd.read_csv(r"tratamientos_estimulacion_predecir.csv")

st.subheader('Datos de los pozos a predecir')
st.write(te_df_pre)

def predict(model, df):
    predictions = predict_model(model, data = df)
    return predictions

if st.button('PREDECIR'):
        st.write('Espere un momento entrenando el modelo...')
        
        #Configurando el moedlo
        s = setup(data=te_df, target = 'Qo desp', ignore_features = "Pozo", html = False, verbose = False)

        # Entrenando el modelo
        model = create_model('rf')     
        
        prediccion = predict(model, te_df_pre)
        
        prediccion["prediction_label"]=prediccion["prediction_label"].astype("int")
             
              
        st.subheader('Pozos con la Predicción de Qo (prediction_label)')
        
        st.dataframe(prediccion.style.set_properties(**{'background-color': 'green','color':'white'}, 
                    subset=["prediction_label"]).format('{:,}', subset=["prediction_label"]))
       
 