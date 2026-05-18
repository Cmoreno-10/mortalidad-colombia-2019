from utils.data_loader import load_data

data = load_data()

data["mortalidad"].to_pickle("data/processed/mortalidad.pkl")
data["causas"].to_pickle("data/processed/causas.pkl")
data["divipola"].to_pickle("data/processed/divipola.pkl")

print("Datos procesados correctamente.")
