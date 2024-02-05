import pandas as pd
import streamlit as st
from pycaret.regression import load_model, predict_model

st.set_page_config(page_title="Predicción de Qo que habrá después de la estimulación")

@st.cache(allow_output_mutation=True)
def get_model():
    return load_model('model_Qo_campo_quesqui')

def predict(model, df):
    predictions = predict_model(model, data = df)
    return predictions['prediction_label'][0]

model = get_model()


st.title("Predicción de Qo que habrá después de la estimulación")
st.markdown("Ingrese los datos para predecir el Qo que habrá después de la estimulación\
     Este modelo fue desarrollado con la librería Pycaret de Pythony la aplicación web\
        fue desarrollada con Streamlit.")

form = st.form("estimulaciones")
solvente = form.number_input('SOLV. [m3]', min_value=1, max_value=500, value = 36)
acido = form.number_input('ACID. [m3]', min_value=1, max_value=500,  value = 27)
quelante = form.number_input('QUEL. [m3]', min_value=1, max_value=500, value = 50)
divergente = form.number_input('DIVER. [m3]', min_value=1, max_value=500, value = 28)
intervalo = form.number_input('Intervalo [md]', min_value=1, max_value=8000, value = 1200)
Qo_antes = form.number_input('Qo antes [bls]', min_value=1, max_value=50000, value = 5353)
 

predict_button = form.form_submit_button('Predecir')

input_dict = {'SOLV. [m3]' : solvente, 'ACID. [m3]' : acido, 'QUEL. [m3]' : quelante, 'DIVER. [m3]' : divergente,
              'Total [m3]' : solvente + acido + quelante + divergente, 'Total acido [m3]' : acido + quelante + divergente,
              'Intervalo [md]' : intervalo, 'Qo antes [bls]' : Qo_antes}
input_df = pd.DataFrame([input_dict])

if predict_button:
    out = predict(model, input_df)
    st.success('La predicción de Qo que habrá después de la estimulación es de: {:,.0f} bls'.format(out))