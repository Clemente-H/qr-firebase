import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from io import StringIO

cred = credentials.Certificate('../firebaseCredentials.json')
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_app = firebase_admin.initialize_app(cred)

# Obtén una referencia al cliente de Firestore
db = firestore.client()

# Función para cargar los datos del CSV a Firestore
def cargar_datos_a_firestore(df):
    # Generar IDs incrementales
    df.index = pd.Series(df.index).apply(lambda x: f"{x+1:03}")
    df.reset_index(inplace=True)
    df.rename(columns={"index": "id"}, inplace=True)
    
    # Cargar cada fila a Firestore
    for index, row in df.iterrows():
        doc_ref = db.collection('Personas').document(row['id'])
        doc_ref.set(row.to_dict())
    
    st.success("Datos cargados con éxito")

# Widget para subir archivo
uploaded_file = st.file_uploader("Selecciona un archivo CSV", type=['csv'])

if uploaded_file is not None:
    # Convertir el archivo cargado en un DataFrame
    stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
    stringio.seek(0)
    df = pd.read_csv(stringio, delimiter=';')
    
    # Previsualizar los datos
    st.write(df)
    
    # Botón para cargar los datos a Firestore
    if st.button("Cargar Datos a Firestore"):
        cargar_datos_a_firestore(df)
