import streamlit as st
from firebase_admin import firestore, credentials, initialize_app
import firebase_admin
# Inicializa Firebase Admin
cred = credentials.Certificate('../firebaseCredentials.json')
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_app = firebase_admin.initialize_app(cred)

# Obtén una referencia al cliente de Firestore
db = firestore.client()

# Función para obtener los datos de Firestore
def obtener_datos():
    docs = db.collection('Ingresos').stream()
    datos = []
    for doc in docs:
        doc_data = doc.to_dict()
        doc_data['id'] = doc.id  # Asegúrate de capturar el ID del documento
        datos.append(doc_data)
    return datos

# Función para borrar un documento en Firestore
def borrar_documento(doc_id):
    db.collection('Ingresos').document(doc_id).delete()

# Función para actualizar un documento en Firestore
def actualizar_documento(doc_id, data):
    db.collection('Ingresos').document(doc_id).set(data, merge=True)

# Mostrar los datos en Streamlit
datos = obtener_datos()
if datos:
    for data in datos:
        with st.expander(f"{data['nombre']}"):
            form = st.form(key=f"form_{data['id']}")
            nombre = form.text_input("Nombre", value=data['nombre'])
            hora_ingreso = form.text_input("Hora de Ingreso", value=data['hora_ingreso'])
            tipo_ingreso = form.selectbox("Tipo de Ingreso", ["normal", "manual"], index=0 if data['tipo_ingreso'] == "normal" else 1)
            id_lugar = form.text_input("ID Lugar", value=data['id_lugar'])
            
            actualizar = form.form_submit_button("Actualizar")
            borrar = form.form_submit_button("Borrar")
            
            if actualizar:
                actualizar_documento(data['id'], {
                    "nombre": nombre,
                    "hora_ingreso": hora_ingreso,
                    "tipo_ingreso": tipo_ingreso,
                    "id_lugar": id_lugar
                })
                st.success("Registro actualizado")
            
            if borrar:
                borrar_documento(data['id'])
                st.success("Registro borrado")
