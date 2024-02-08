#importar librerias
import streamlit as st
import pandas as pd
from pycaret.regression import load_model, predict_model

@st.cache_resource
def get_model():
    return load_model('model_Ptp_estimulaciones')

def predict(model, df):
    predictions = predict_model(model, data = df)
    return predictions['prediction_label'][0]

model = get_model()

def main():
    st.sidebar.image('SmartBI.png')
    #titulo
    st.title('Predicción de Ptp que habrá después de la estimulación')
    #titulo de sidebar
    st.sidebar.header('Ingresar los siguientes parámetros:')

    #funcion para poner los parametrso en el sidebar
    def parametros_usuario():
        
        solvente = st.sidebar.number_input('SOLV. [m3]', min_value=1, max_value=500, value = 36)
        acido = st.sidebar.number_input('ACID. [m3]', min_value=1, max_value=500,  value = 27)
        quelante = st.sidebar.number_input('QUEL. [m3]', min_value=1, max_value=500, value = 50)
        divergente = st.sidebar.number_input('DIVER. [m3]', min_value=1, max_value=500, value = 28)
        intervalo = st.sidebar.number_input('Intervalo [md]', min_value=1, max_value=8000, value = 1200)
        Qo_antes = st.sidebar.number_input('Qo antes [bls]', min_value=1, max_value=50000, value = 5353)
        Ptp_antes = st.sidebar.number_input('Ptp antes [kg/cm2]', min_value=1, max_value=2000, value = 300)
             
        input_dict = {'SOLV. [m3]' : solvente, 'ACID. [m3]' : acido, 'QUEL. [m3]' : quelante, 'DIVER. [m3]' : divergente,
                      'Total [m3]' : solvente + acido + quelante + divergente, 'Total acido [m3]' : acido + quelante + divergente,
                      'Intervalo [md]' : intervalo, 'Qo antes [bls]' : Qo_antes, 'Ptp antes [kg/cm2]' : Ptp_antes}
        
        input_df = pd.DataFrame([input_dict])
        
        return input_df

    df = parametros_usuario()
   
    
    st.subheader('Parámetros de entrada')
  
    st.write(df)

    if st.button('PREDECIR'):
        out = predict(model, df)
        st.success('La predicción de Ptp que habrá después de la estimulación es de: {:,.0f} Kg/cm2'.format(out))


if __name__ == '__main__':
    main()
    