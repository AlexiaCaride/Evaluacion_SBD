import pandas as pd
import pymongo

def get_mongo_client():
    try:
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        return client
    except pymongo.errors.ConnectionFailure as e:
        print(f"Error de conexión con MongoDB: {e}")
        return None

client = get_mongo_client()
if client:
    db = client["bicicorunha_db"]
    collection = db["data"]
else:
    print("No se pudo conectar a MongoDB, saíndo.")
    exit(1)

try:
    documents = collection.find()

    data = []
    for doc in documents:
        data.append({
        "id": doc.get("id"),
        "name": doc.get("name"),
        "timestamp": doc.get("timestamp"),
        "free_bikes": doc.get("free_bikes"),
        "empty_slots": doc.get("empty_slots"),
        "uid": doc.get("extra", {}).get("uid"),
        "last_updated": doc.get("extra", {}).get("last_updated"),
        "slots": doc.get("extra", {}).get("slots"),
        "normal_bikes": doc.get("extra", {}).get("normal_bikes"),
        "ebikes": doc.get("extra", {}).get("ebikes")
    })

    df = pd.DataFrame(data)

    if not df.empty:
        csv_filename = "bicicorunha_data.csv"
        df.to_csv(csv_filename, index=False)
        print(f"Datos exportados correctamente a {csv_filename}")

        parquet_filename = "bicicorunha_data.parquet"
        df.to_parquet(parquet_filename, index=False)
        print(f"Datos exportados correctamente a {parquet_filename}")
    else:
        print("No se encontraron datos para exportar.")

except Exception as e:
    print(f"Error al procesar los datos: {e}")