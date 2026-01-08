from pathlib import Path
import pandas as pd

carpeta = Path(r"C:\Users\ikerr\Code\TFG\Datasets\JeffSackmann\tennis_atp-master")
salida = carpeta / "merge_atp_matches.csv"

SEP = None

archivo = sorted(carpeta.glob("atp_matches_*.csv"))
dfs = []

for f in archivo:
    sep = SEP
    if sep is None:
        # prueba delimitadores comunes
        for candidato in [",", ";", "\t", "|"]:
            try:
                tmp = pd.read_csv(f, nrows=200, sep=candidato, engine="python", on_bad_lines="skip")
                sep = candidato
                break
            except Exception:
                continue

    # lee el archivo completo
    df = pd.read_csv(
        f, sep=sep, engine="python",
        on_bad_lines="skip",  # ignora líneas mal formadas
        encoding_errors="ignore"  # por si hay caracteres raros
    )
    df["__source_file"] = f.name  # útil para rastrear origen
    dfs.append(df)
    print(f"{f.name} complete!")

# Unir por columnas (union de esquema)
# Rellena con NaN las columnas que no existan en algunos ficheros
merged = pd.concat(dfs, ignore_index=True, sort=False)

# (opcional) ordena columnas: primero las comunes y al final __source_file
cols = [c for c in merged.columns if c != "__source_file"] + ["__source_file"]
merged = merged[cols]

# Guardar en CSV y también en Parquet (mucho más rápido para trabajar)
merged.to_csv(salida, index=False)
merged.to_parquet(carpeta / "merge_todos.parquet", index=False)
print(f"Listo: {salida}")