import requests
import pymongo
import schedule
import time
from datetime import datetime

# Conexión a MongoDB
def get_mongo_client():
    try:
        # Conectar al contenedor o servidor de MongoDB
        client = pymongo.MongoClient("mongodb://mongo:27017/")  # Cambia la URL si es necesario
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

# Función para obtener y almacenar los datos
def fetch_and_store_data(collection):
    # URL de la API
    url = "https://api.citybik.es/v2/networks/bicicorunha"

    try:
        # Realizar solicitud GET a la API
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la respuesta no es exitosa

        # Obtener los datos de la API
        data = response.json()

        # Extraer las estaciones
        stations = data.get('network', {}).get('stations', [])

        if stations:
            # Añadir fecha y hora de la inserción
            timestamp = datetime.now().isoformat()

            # Agregar el timestamp a cada estación
            for station in stations:
                station['timestamp'] = timestamp

            # Guardar las estaciones en MongoDB
            result = collection.insert_many(stations)  # Insertar múltiples estaciones
            print(f"Se han insertado {len(result.inserted_ids)} estaciones en MongoDB con timestamp: {timestamp}")
        else:
            print("No se encontraron estaciones en la respuesta.")

    except requests.exceptions.RequestException as e:
        print(f"Error al conectar a la API: {e}")
    except Exception as e:
        print(f"Error al guardar los datos en MongoDB: {e}")

# Inserta el primer dato al inicio
fetch_and_store_data(collection)

# Programar la ejecución cada 3 minutos
schedule.every(3).minutes.do(fetch_and_store_data, collection=collection)

# Mantener el script en ejecución
try:
    while True:
        schedule.run_pending()  # Ejecuta las tareas programadas si es necesario
        time.sleep(1)  # Espera 1 segundo antes de comprobar de nuevo
except KeyboardInterrupt:
    print("\nDesconexión manual detectada. El script fue detenido correctamente.")

