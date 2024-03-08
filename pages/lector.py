import streamlit as st
import pandas as pd
from datetime import datetime
from pathlib import Path
import re  # Importar el módulo de expresiones regulares
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app
from datetime import datetime

cred = credentials.Certificate('../firebaseCredentials.json')
try:
    firebase_app = firebase_admin.get_app()
except ValueError:
    firebase_app = firebase_admin.initialize_app(cred)

# Obtén una referencia al cliente de Firestore
db = firestore.client()


# Campo de entrada para el código escaneado
codigo_escaneado = st.text_input("Escanear Código de Barras o QR", key="input")

# Función para buscar un RUT en Firestore
def buscar_rut_en_firestore2(rut_buscado):
    # Buscar todos los documentos en la colección 'Personas' que tengan el RUT especificado
    docs = db.collection('Personas').where('Rut', '==', rut_buscado).stream()
    
    # Convertir los documentos encontrados en una lista para verificar si está vacía o no
    docs_list = list(docs)
    if docs_list:
        return True  # El RUT está en la colección
    else:
        return False  # El RUT no se encontró en la colección
    
# Función para buscar un RUT en Firestore y obtener el nombre completo si se encuentra
def buscar_rut_en_firestore(rut_buscado):
    # Buscar todos los documentos en la colección 'Personas' que tengan el RUT especificado
    docs = db.collection('Personas').where('Rut', '==', rut_buscado).stream()
    
    # Convertir los documentos encontrados en una lista
    docs_list = list(docs)
    
    # Si se encontró al menos un documento, devolver el nombre y apellido concatenados
    if docs_list:
        doc_data = docs_list[0].to_dict()
        nombre = doc_data.get('Nombre', "")
        apellido = doc_data.get('Apellido', "")
        nombre_completo = f"{nombre} {apellido}".strip()
        return nombre_completo
    else:
        # Si no se encuentra el RUT, devolver None
        return None





# Intenta extraer el RUN del código escaneado automáticamente tras el escaneo
if "RUN¿" in codigo_escaneado:
    try:
        # Extraer el RUN del texto escaneado y limpiar el caracter extra
        run_escaneado = re.search("RUN¿(.*?)/type", codigo_escaneado).group(1).replace("'", "-")
        
        # Mostrar el RUN extraído para confirmación visual
        st.write(f"RUN escaneado: {run_escaneado}")
        nombre = buscar_rut_en_firestore(run_escaneado)
        if nombre:
            #st.success("El RUT está presente en la colección.")
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            ingreso = {"nombre":nombre, "hora_ingreso":current_time, "rut":run_escaneado, "tipo_ingreso":"normal", "id_lugar":"001"}
            doc_ref = db.collection('Ingresos').add(ingreso)
            st.success('Persona con entrada Valida. Ingreso: ' + str(current_time))
        else:
            st.error("El RUT no se encontró en la colección.")
        
    except AttributeError:
        # En caso de que el patrón de búsqueda no encuentre una coincidencia
        st.error("Formato de código QR inválido.")


# if run:
#             if df['Rut'].isin([str(run)]).any():

#                 import streamlit as st
#                 # Obtener el tiempo actual
#                 now = datetime.now()
#                 # Formatear el tiempo como deseas. Aquí estoy usando formato año-mes-día hora:minuto:segundo
#                 current_time = now.strftime("%Y-%m-%d %H:%M:%S")
#                 st.success('Persona con entrada Valida. Ingreso: ' + str(current_time))

#             else:
#                 st.error('Persona con entrada no Valida')