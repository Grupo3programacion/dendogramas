from BibtexReader import BibtexReader

# Cargar los archivos BibTeX
used_reader = BibtexReader("todo_filtrado_final.bib")
unused_reader = BibtexReader("archivos_no_utilizados.bib")

used_entries = used_reader.load_entries()
unused_entries = unused_reader.load_entries()

# Obtener los IDs normalizados
used_ids = {entry.get("ID", "").strip().lower() for entry in used_entries if "ID" in entry}
unused_ids = {entry.get("ID", "").strip().lower() for entry in unused_entries if "ID" in entry}

# Mostrar estadísticas
print(f"📂 Total de entradas en `todo_filtrado_final.bib`: {len(used_entries)}")
print(f"📂 Total de entradas en `archivos_no_utilizados.bib`: {len(unused_entries)}")

# Comparar IDs
unmatched_ids = unused_ids - used_ids  # IDs que están en archivos_no_utilizados pero no en todo_filtrado

print(f"❌ Archivos sin coincidencias: {len(unmatched_ids)}")
if unmatched_ids:
    print("📌 Ejemplos de IDs no utilizados:", list(unmatched_ids)[:10])
else:
    print("✅ Todos los archivos en `archivos_no_utilizados.bib` están en `todo_filtrado_final.bib`")
