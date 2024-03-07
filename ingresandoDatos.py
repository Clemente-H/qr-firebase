import firebase_admin as firebaseAdmin
from firebase_admin import firestore
from firebase_admin import credentials
# Ruta al archivo de credenciales descargado
cred = credentials.Certificate('firebaseCredentials.json')
# Inicializa la aplicación con las credenciales
firebaseAdmin.initialize_app(cred)
# Obtén una referencia al servicio de Firestore

# Obtén una referencia al cliente de Firestore
db = firestore.client()

# Datos a ingresar, reemplaza esto con la variable `filas` de arriba
datos = [
    {"id": "438274591", "nombre": "Carlos López", "hora_ingreso": "2024-03-07 18:13:00", "tipo_ingreso": "normal", "id_lugar": "004"},
    {"id": "420625729", "nombre": "Sofía Martínez", "hora_ingreso": "2024-03-07 16:17:00", "tipo_ingreso": "manual", "id_lugar": "002"},
    {"id": "460859608", "nombre": "Carlos Flores", "hora_ingreso": "2024-03-07 12:43:00", "tipo_ingreso": "manual", "id_lugar": "004"},
    {"id": "993406879", "nombre": "Luis Hernández", "hora_ingreso": "2024-03-07 11:26:00", "tipo_ingreso": "normal", "id_lugar": "004"},
    {"id": "507460900", "nombre": "Sofía Flores", "hora_ingreso": "2024-03-07 08:09:00", "tipo_ingreso": "manual", "id_lugar": "002"},
    {"id": "214671040", "nombre": "Carmen Martínez", "hora_ingreso": "2024-03-07 21:19:00", "tipo_ingreso": "manual", "id_lugar": "001"},
    {"id": "129234314", "nombre": "Luis Ramírez", "hora_ingreso": "2024-03-07 06:37:00", "tipo_ingreso": "normal", "id_lugar": "002"},
    {"id": "141393314", "nombre": "Ana López", "hora_ingreso": "2024-03-07 20:42:00", "tipo_ingreso": "normal", "id_lugar": "002"},
    {"id": "326705477", "nombre": "Carlos López", "hora_ingreso": "2024-03-07 22:21:00", "tipo_ingreso": "normal", "id_lugar": "005"},
    {"id": "759213351", "nombre": "Carmen Flores", "hora_ingreso": "2024-03-07 15:04:00", "tipo_ingreso": "manual", "id_lugar": "003"}
]

# Ingresa los datos en Firestore
for fila in datos:
    # Puedes cambiar 'nombre_de_tu_coleccion' por el nombre real de tu colección en Firestore
    doc_ref = db.collection('Ingresos').document(fila["id"])
    doc_ref.set(fila)
