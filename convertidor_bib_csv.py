import bibtexparser
import pandas as pd
import os

def convertir_bib_a_csv(ruta_bib="todo_filtrado_final.bib", ruta_csv="BD.csv"):
    if not os.path.exists(ruta_bib):
        raise FileNotFoundError(f"No se encontró el archivo .bib en la ruta: {ruta_bib}")

    with open(ruta_bib, encoding="utf-8") as bibtex_file:
        bib_database = bibtexparser.load(bibtex_file)

    registros = []
    for entry in bib_database.entries:
        registros.append({
            "titulo": entry.get("title", ""),
            "autor": entry.get("author", ""),
            "año": entry.get("year", ""),
            "palabras_clave": entry.get("keywords", ""),
            "abstract": entry.get("abstract", "")
        })

    df = pd.DataFrame(registros)
    df.to_csv(ruta_csv, index=False)
    print(f"✅ Archivo CSV generado exitosamente en: {ruta_csv}")

# 👇 Agrega esto para que se ejecute directamente
if __name__ == "__main__":
    convertir_bib_a_csv()
