import streamlit as st
import pandas as pd
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

cred = credentials.Certificate('../firebaseCredentials.json')
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_app = firebase_admin.initialize_app(cred)

# Obtén una referencia al cliente de Firestore
db = firestore.client()

# Función para obtener los datos de Firestore y convertirlos en un DataFrame de Pandas
def obtener_datos():
    query = db.collection('Ingresos').stream()
    docs = [{**doc.to_dict(), 'id': doc.id} for doc in query]  # Incluye el 'id' del documento
    if docs:
        df = pd.DataFrame(docs)
        # Ordena las columnas específicamente
        df = df[['id', 'nombre', 'tipo_ingreso', 'hora_ingreso', 'id_lugar']]
    else:
        df = pd.DataFrame(columns=['id', 'nombre', 'tipo_ingreso', 'hora_ingreso', 'id_lugar'])
    return df

# Función para actualizar Firestore basado en el DataFrame editado
def actualizar_firestore(df):
    for index, row in df.iterrows():
        doc_ref = db.collection('Ingresos').document(row['id'])
        # Convierte la fila del DataFrame a diccionario y elimina la clave 'id' antes de actualizar
        doc_data = row.to_dict()
        doc_data.pop('id', None)  # Elimina 'id' ya que no lo queremos como campo en el documento
        doc_ref.set(doc_data)

# Cargar datos de Firestore y mostrarlos en st.data_editor
df = obtener_datos()
df_editado = st.data_editor(data=df)

# Botón para guardar cambios
if st.button("Guardar cambios"):
    actualizar_firestore(df_editado)
    st.experimental_rerun()  # Rerun the script to refresh the data shown
