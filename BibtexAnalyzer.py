# bibtex_analyzer.py
from io import BytesIO
from flask import jsonify  # Asegúrate de importar jsonify
import base64
import random
import networkx as nx
from collections import Counter
from flask import Flask
from BibtexReader import BibtexReader
import os
import logging
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re  # Importa la librería para expresiones regulares
from diccionario.diccionario import CATEGORIES  # Importamos CATEGORIES desde diccionario.py
from diccionario.countries import countries  # Importamos la lista de países desde countries.py


EQUIVALENCES = {
    "Classical Test Theory": ["Classical Test Theory", "CTT"],
    "Confirmatory Factor Analysis": ["Confirmatory Factor Analysis", "CFA"],
    "Exploratory Factor Analysis": ["Exploratory Factor Analysis", "EFA"],
    "Item Response Theory": ["Item Response Theory", "IRT"],
    "Structural Equation Model": ["Structural Equation Model", "SEM"],
}


class BibtexAnalyzer:
    def __init__(self):
        """
        Inicializa el analizador con las entradas de BibTeX y las equivalencias de variables.
        """
        # Asegúrate de que el archivo .bib esté en la ubicación correcta
        file_path = os.path.join(os.path.dirname(__file__), 'todo_filtrado_final.bib')
        self.reader = BibtexReader(file_path)
        self.categories = CATEGORIES
        self.equivalences = EQUIVALENCES
        self.frequencyTable = None  # Inicializa como None o un diccionario vacío
        self.entries = self.reader.load_entries()
        self.graph = nx.Graph()

    
#ANALIZAR ARCHIVO NO UTLIZADO
   
    def analyze_unused_files(self, tipo="JOUR"):
        """
        Analiza los archivos no utilizados y filtra por tipo de entrada.
        """
        unused_path = os.path.join(os.path.dirname(__file__), 'archivos_no_utilizados.bib')

        if not os.path.exists(unused_path):
            return jsonify({"status": "error", "message": "⚠️ El archivo `archivos_no_utilizados.bib` no existe."})

        with open(unused_path, 'r', encoding='utf-8') as file:
            data = file.read()

        data = data.replace("\u00a0", " ")  # Eliminar caracteres invisibles
        entries = re.split(r"\n?ER\s*-\s*\n?", data)

        print(f"📄 Total de entradas detectadas: {len(entries)}")

        unused_entries = []
        for entry in entries:
            lines = entry.strip().split("\n")
            entry_dict = {}

            for line in lines:
                if " - " in line:
                    key, value = line.split(" - ", 1)
                    entry_dict[key.strip()] = value.strip()

            if entry_dict and entry_dict.get("TY", "") == tipo:  # Filtrar por tipo de entrada
                unused_entries.append(entry_dict)

        print(f"📄 Total de entradas filtradas ({tipo}): {len(unused_entries)}")

        response = {
            "status": "success",
            "total_entries": len(unused_entries),
            "missing_fields": {
                "T1 (Título)": sum(1 for entry in unused_entries if not entry.get('T1')),
                "AU (Autor)": sum(1 for entry in unused_entries if not entry.get('AU')),
                "PY (Año)": sum(1 for entry in unused_entries if not entry.get('PY')),
            },
        }

        return jsonify(response)






##REQUISITO 2

    def plot_graph(self, variable1, variable2):
        """
        Dibuja un gráfico basado en las dos variables proporcionadas,
        limitando a los 15 pares más frecuentes y devuelve el gráfico
        como una imagen en formato base64.
        """
        # Inicializamos las listas de agrupación
        var1_values = []
        var2_values = []
        
        # Extraemos las variables correspondientes de cada entrada
        for entry in self.entries:
            if variable1 in entry and variable2 in entry:
                var1_values.append(entry[variable1])
                var2_values.append(entry[variable2])

        # Contamos las ocurrencias de cada par de valores
        data = Counter(zip(var1_values, var2_values))

        # Ordenamos los resultados por cantidad de publicaciones (en orden descendente)
        top_data = data.most_common(15)

        # Separar los resultados para graficarlos
        labels = [f"{v[0][0]} - {v[0][1]}" for v in top_data]
        counts = [v[1] for v in top_data]
        
        # Crear el gráfico
        plt.figure(figsize=(10, 6))
        plt.barh(labels, counts, color='skyblue')
        plt.title(f'Publicaciones por {variable1} y {variable2}')
        plt.xlabel('Cantidad de Publicaciones')
        plt.ylabel(f'{variable1} - {variable2}')
        plt.tight_layout()

        # Convertir la imagen del gráfico a base64
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')  # Guarda la imagen en el buffer de memoria
        plt.close()  # Cerrar la figura para liberar memoria
        img_buffer.seek(0)
        
        # Convertir el contenido del buffer en base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return img_base64

##REQUISITO 3
    def analyze_frequency(self):
        """
        Analiza la frecuencia de aparición de las variables en los abstracts.
        :return: Diccionario con la frecuencia de las variables por categoría.
        """
        logging.debug("Iniciando la ejecución de analyze_frequency...")
        
        frequency_data = {}

        # Inicializa el diccionario por cada categoría
        for category in self.categories:
            frequency_data[category] = {}

        # Procesar los abstracts
        for entry in self.entries:
            abstract = entry.get('abstract', '').lower()  # Convertir el abstract a minúsculas

            for category, variables in self.categories.items():
                for variable in variables:
                    # Unificar las equivalencias
                    for eq in self.equivalences.get(variable, [variable]):
                        eq_lower = eq.lower()

                        # Si la variable contiene un guion, dividir en ambas partes y contar cada una
                        if "-" in eq_lower:
                            part1, part2 = map(str.strip, eq_lower.split("-", 1))
                            count = abstract.count(part1) + abstract.count(part2)
                        else:
                            count = abstract.count(eq_lower)

                        # Agregar el conteo al diccionario de frecuencias
                        if eq_lower not in frequency_data[category]:
                            frequency_data[category][eq_lower] = 0
                        frequency_data[category][eq_lower] += count

            # Ordenar cada categoría de mayor a menor frecuencia
        for category in frequency_data:
            frequency_data[category] = dict(
                sorted(frequency_data[category].items(), key=lambda item: item[1], reverse=True)
            )


            logging.debug("Finalizando analyze_frequency...")
            self.frequencyTable = frequency_data  # Actualiza el atributo de instancia
            return frequency_data


##REQUISITO 4
    def plot_word_cloud(self):
        """
        Genera y devuelve una nube de palabras en formato base64.
        """
        # Combinar todas las frecuencias en un solo diccionario
        combined_frequencies = {}
        for category, words in self.frequencyTable.items():
            for word, freq in words.items():
                combined_frequencies[word] = combined_frequencies.get(word, 0) + freq

        # Generar la nube de palabras
        wordcloud = WordCloud(width=800, height=400, background_color="white").generate_from_frequencies(combined_frequencies)

        # Convertir la imagen de la nube de palabras a base64
        img_buffer = BytesIO()
        wordcloud.to_image().save(img_buffer, format="PNG")
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        
        return img_base64

##REQUISITO 5
    def get_top_10_journals(self):
        """
        Identifica los 10 journals con la mayor cantidad de artículos publicados.
        Si un artículo no tiene el nombre del journal, se utiliza el campo ISSN.
        
        :return: Lista de los 10 journals con más artículos publicados.
        """
        journal_counts = {}

        for entry in self.entries:
            journal_name = entry.get('journal') or entry.get('issn')
            if journal_name:
                journal_counts[journal_name] = journal_counts.get(journal_name, 0) + 1

        self.top_10_journals = sorted(journal_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return self.top_10_journals

    def get_top_articles_with_random_country(self):
        """
        Para cada uno de los 10 journals principales, selecciona los primeros 5 artículos
        y asigna un país aleatorio a cada uno.
        
        :return: Diccionario con los journals y una lista de los 5 artículos con país asignado.
        """

        
        journal_articles = {}

        for journal in self.top_10_journals:
            journal_id = journal[0]
            articles = [entry for entry in self.entries if entry.get('journal') == journal_id or entry.get('issn') == journal_id]
            selected_articles = articles[:5]

            articles_with_countries = [
                {
                    'title': article.get('title', 'No title'),
                    'country': random.choice(countries)
                }
                for article in selected_articles
            ]

            journal_articles[journal_id] = articles_with_countries

        return journal_articles

    def create_graph(self):
        """
        Crea el grafo que relaciona journals, artículos y países.
        """
        self.get_top_10_journals()  # Asegurarse de obtener y almacenar los 10 journals
        journal_articles = self.get_top_articles_with_random_country()

        for journal, articles in journal_articles.items():
            self.graph.add_node(journal, type='journal')

            for article_info in articles:
                article_title = article_info['title']
                country = article_info['country']

                self.graph.add_node(article_title, type='article')
                self.graph.add_node(country, type='country')

                # Crear las aristas (edges) entre los journals, artículos y países
                self.graph.add_edge(journal, article_title)
                self.graph.add_edge(article_title, country)

    def generate_graph(self):
        """
        Genera y devuelve el grafo en formato base64.
        """
        pos = nx.spring_layout(self.graph, k=1, iterations=50)
        journals = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "journal"]
        articles = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "article"]
        countries = [node for node, attr in self.graph.nodes(data=True) if attr["type"] == "country"]

        # Crear la figura del grafo
        plt.figure(figsize=(25, 25))
        nx.draw_networkx_nodes(self.graph, pos, nodelist=journals, node_color="lightcoral", node_size=2000, label="Journals")
        nx.draw_networkx_nodes(self.graph, pos, nodelist=articles, node_color="skyblue", node_size=1500, label="Articles")
        nx.draw_networkx_nodes(self.graph, pos, nodelist=countries, node_color="lightgreen", node_size=1000, label="Countries")
        nx.draw_networkx_edges(self.graph, pos, edge_color="gray", alpha=0.5)
        nx.draw_networkx_labels(self.graph, pos, font_size=5, font_weight="bold")

        # Convertir la figura del grafo a base64 en lugar de guardarla en el disco
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')  # Guarda la imagen en el buffer de memoria
        plt.close()  # Cerrar la figura para liberar memoria
        img_buffer.seek(0)
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')

        return img_base64
    
#archivos no utilzados
'''    def analyze_unused_files(self):
        """
        Analiza los archivos no utilizados en comparación con las entradas cargadas y devuelve un resumen estadístico.
        """
        unused_path = os.path.join(os.path.dirname(__file__), 'archivos_no_utilizados.bib')

        if not os.path.exists(unused_path):
            return "⚠️ El archivo de archivos no utilizados no existe."

        unused_reader = BibtexReader(unused_path)
        unused_entries = unused_reader.load_entries()

        total_unused = len(unused_entries)
        total_used = len(self.entries)
        
        if total_unused == 0:
            return "✅ No hay archivos no utilizados."

        # Normalizar los IDs para evitar problemas de comparación (espacios, mayúsculas, etc.)
        used_ids = {entry.get("ID", "").strip().lower() for entry in self.entries if "ID" in entry}
        unused_ids = [
            entry for entry in unused_entries if entry.get("ID", "").strip().lower() not in used_ids
        ]

        count_unused = len(unused_ids)
        count_matched = total_unused - count_unused  # Archivos que sí se encontraron en el otro archivo

        return (
            f"🔎 **Análisis de Archivos No Utilizados:**\n\n"
            f"📂 **Total en `archivos_no_utilizados.bib`**: {total_unused}\n"
            f"📂 **Total en `todo_filtrado_final.bib`**: {total_used}\n"
            f"✅ **Coincidencias encontradas**: {count_matched}\n"
            f"❌ **Archivos sin coincidencias**: {count_unused}\n\n"
            f"📌 Esto significa que **{count_unused} archivos** no tienen correspondencia en los datos utilizados."
        ) '''



