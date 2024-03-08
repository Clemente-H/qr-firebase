import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from st_pages import Page, add_page_title, show_pages
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib import Path
import re  # Importar el módulo de expresiones regulares

# cred = credentials.Certificate('../firebaseCredentials.json')
# print(cred)
# firebase_admin.initialize_app(cred)
# db = firestore.client()



"## Declaring the pages in your app:"

show_pages(
    [
        Page("./app.py", "Home", "🏠"),
        # Can use :<icon-name>: or the actual icon
        Page("./registros.py", "Registros", ":books:"),
        Page("./lector.py", "lector", ":books:"),
        Page("./addPermissions.py", "Subir Datos", ":books:"),
        
    ]
)

add_page_title()  # Optional method to add title and icon to current page


# Suponiendo que PersonasAllowed.csv está en el mismo directorio que tu script
df = pd.read_csv('../PersonasAllowed.csv' ,delimiter=';')

# Campo de entrada para el código escaneado
codigo_escaneado = st.text_input("Escanear Código de Barras o QR", on_change=None, key="input")

# Intenta extraer el RUN del código escaneado automáticamente tras el escaneo
run_escaneado = ""
if "RUN¿" in codigo_escaneado:
    try:
        # Extraer el RUN del texto escaneado y limpiar el caracter extra
        run_escaneado = re.search("RUN¿(.*?)/type", codigo_escaneado).group(1).replace("'", "")
        
        # Verificar si el RUN está en el DataFrame
        if df['Rut'].isin([run_escaneado]).any():
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            st.success(f'Persona con entrada Válida. Ingreso: {current_time}')
            st.experimental_rerun()  # Recarga la página para limpiar el campo de entrada
        else:
            st.error('Persona con entrada no Válida')
            st.experimental_rerun()  # Recarga la página para limpiar el campo de entrada
            
    except AttributeError:
        # En caso de que el patrón de búsqueda no encuentre una coincidencia
        st.error("Formato de código QR inválido.")
        st.experimental_rerun()  # Recarga la página para limpiar el campo de entrada