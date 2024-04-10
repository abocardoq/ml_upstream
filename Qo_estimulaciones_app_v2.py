#importar librerias
import streamlit as st
import pandas as pd
from pycaret.regression import *

#Cargando datos
tratamiento_estimulacion_df = pd.read_csv(r"tratamientos_estimulacion.csv")

def predict(model, df):
    predictions = predict_model(model, data = df)
    return predictions['prediction_label'][0]


def main():
    st.sidebar.image('SmartBI.png')
    #titulo
    st.title('Predicción de Qo que habrá después de la estimulación')
    #titulo de sidebar
    st.sidebar.header('Ingresar los siguientes parámetros:')

    #funcion para poner los parametrso en el sidebar
    def parametros_usuario():
        
        solvente = st.sidebar.number_input('Solvente', min_value=1, max_value=500, value = 36)
        acido = st.sidebar.number_input('Acido', min_value=1, max_value=500,  value = 27)
        quelante = st.sidebar.number_input('Quelante', min_value=1, max_value=500, value = 50)
        divergente = st.sidebar.number_input('Divergente', min_value=1, max_value=500, value = 28)
        intervalo = st.sidebar.number_input('Intervalo', min_value=1, max_value=8000, value = 1200)
        Qo_antes = st.sidebar.number_input('Qo antes', min_value=1, max_value=50000, value = 5353)
             
        input_dict = {'solvente' : solvente, 'acido' : acido, 'quelante' : quelante, 'divergente' : divergente,
                                            'Intervalo' : intervalo, 'Qo antes' : Qo_antes}
        
        input_df = pd.DataFrame([input_dict])
        
        return input_df

    df = parametros_usuario()
   
    
    st.subheader('Parámetros de entrada')
  
    st.write(df)

    if st.button('PREDECIR'):
        st.subheader('Espere un momento entrenando el modelo...')
        
        #Configurando el moedlo
        s = setup(data=tratamiento_estimulacion_df, target = 'Qo desp', ignore_features = "Pozo", html = False, verbose = False)

        # Entrenando el modelo
        model = create_model('rf')
        
        out = predict(model, df)
        st.success('La predicción de Qo que habrá después de la estimulación es de: {:,.0f} bls'.format(out))


if __name__ == '__main__':
    main()
    