import os
import json

# Directorio donde se encuentran los archivos GeoJSON
directory = r"C:\Users\Juan Dallos\Desktop\NNAavaluo"

# Lista para almacenar los datos de todos los archivos
all_features = []

# Leer y combinar los archivos GeoJSON
for filename in os.listdir(directory):
    if filename.endswith(".geojson"):
        with open(os.path.join(directory, filename), 'r') as geojson_file:
            geojson_data = json.load(geojson_file)
            all_features.extend(geojson_data['features'])

# Crear un GeoJSON final con todos los datos combinados
final_geojson = {
    "type": "FeatureCollection",
    "features": all_features
}

# Guardar el GeoJSON final en un archivo
with open("todos_los_datos.geojson", 'w') as output_file:
    json.dump(final_geojson, output_file, indent=2)
