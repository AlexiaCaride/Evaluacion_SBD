import requests
import pymongo
import schedule
import time
from datetime import datetime

def get_mongo_client():
    try:
        client = pymongo.MongoClient("mongodb://mongo:27017/")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error de conexión con MongoDB: {e}")
        return None

# Conectar a MongoDB
client = get_mongo_client()
if client:
    db = client["bicicorunha_db"]
    collection = db["data"]
else:
    print("No se pudo conectar a MongoDB.")
    exit(1)

# Función para obtener y almacenar datos
def fetch_and_store_data():
    url = "http://api.citybik.es/v2/networks/bicicorunha"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa
        data = response.json()

        # Añadir fecha y hora de la inserción
        data['timestamp'] = datetime.now().isoformat()

        # Guardar los datos en MongoDB
        collection.insert_one(data)
        print(f"Datos guardados correctamente en MongoDB: {data['timestamp']}")
    except requests.exceptions.RequestException as e:
        print(f"Error al conectar a la API: {e}")
    except Exception as e:
        print(f"Error al guardar los datos en MongoDB: {e}")

# Inserta el primer dato al inicio
fetch_and_store_data()

# Programar la ejecución cada 30 segundos
schedule.every(3).minutes.do(fetch_and_store_data)

# Mantener el script en ejecución
try:
    while True:
        schedule.run_pending()  # Ejecuta las tareas programadas si es necesario
        time.sleep(1)  # Espera 1 segundo antes de comprobar de nuevo
except KeyboardInterrupt:
    # Aquí manejamos la desconexión manual
    print("\nDesconexión manual detectada. El script fue detenido correctamente.")

