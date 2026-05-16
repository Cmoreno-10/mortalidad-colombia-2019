from utils.data_loader import load_data

data = load_data()

print("Bases cargadas correctamente")
print(data.keys())

mortalidad = data["mortalidad"]

print("Filas:", mortalidad.shape[0])
print("Columnas:", mortalidad.shape[1])
print(mortalidad.head())
print(mortalidad.columns)
