from flask import Flask, render_template, request, jsonify, send_file
import io
import matplotlib
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.cluster.hierarchy import dendrogram, linkage
import uuid
import os
import base64
from io import BytesIO
from jerarquico import ejecutar_agrupamiento_jerarquico


matplotlib.use('Agg')  # Establece el backend a uno sin GUI
import matplotlib.pyplot as plt
import random
from flask_cors import CORS
# En app.py
from BibtexAnalyzer import BibtexAnalyzer
app = Flask(__name__)  # Primero creas la aplicación Flask
CORS(app)  # Luego habilitas CORS para todas las rutas

# Ruta principal para servir la interfaz
@app.route('/')
def home():
    print("📢 Cargando index.html...")  # Mensaje en la terminal
    return render_template('index.html')


# Endpoint para generar estadísticos (Requerimiento 2 - 4 gráficos)
@app.route('/generar_grafico', methods=['POST'])
def estadisticos():
    # Obtén los valores de variable1 y variable2 desde la solicitud o usa valores predeterminados
    variable1 = request.json.get('variable1')
    variable2 = request.json.get('variable2')
    
    # Crea una instancia del analizador y genera el gráfico
    analyzer = BibtexAnalyzer()
    wordcloud_base64 = analyzer.plot_graph(variable1, variable2)
    
    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})


@app.route('/frecuencia', methods=['GET'])
def frecuencia():
    """
    Endpoint para analizar la frecuencia de aparición de variables en los abstracts.
    """
    # Crear una instancia de BibtexAnalyzer
    analyzer = BibtexAnalyzer()

    # Ejecutar el análisis de frecuencia
    frequency_data = analyzer.analyze_frequency()

    # Retornar los datos de frecuencia como respuesta JSON
    return jsonify({'status': 'success', 'data': frequency_data})

@app.route('/nube_palabras', methods=['GET'])
def nube_palabras():
    """
    Endpoint para generar una nube de palabras y retornarla en formato base64.
    """
    analyzer = BibtexAnalyzer()
    # Asegúrate de haber ejecutado `analyze_frequency` previamente para tener `frequencyTable` completo
    analyzer.analyze_frequency()
    
    # Generar la nube de palabras
    wordcloud_base64 = analyzer.plot_word_cloud()
    
    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})

@app.route('/generar_grafo', methods=['GET'])
def generar_grafo():
    analyzer = BibtexAnalyzer()
    # Llama a la función que genera el grafo
    analyzer.create_graph()  # Primero crea el grafo con nodos y aristas
    wordcloud_base64 = analyzer.generate_graph()  # Luego genera la disposición y configuración del grafo

    # Devolver la imagen de la nube de palabras en formato base64
    return jsonify({'status': 'success', 'data': wordcloud_base64})

@app.route('/archivos_no_utilizados', methods=['GET'])
def archivos_no_utilizados():
    tipo = request.args.get('tipo', 'JOUR')  # Si no se envía nada, usa JOUR por defecto
    analyzer = BibtexAnalyzer()
    return analyzer.analyze_unused_files(tipo)

@app.route('/generar-dendograma', methods=['POST'])
def generar_dendograma():
    resultado = ejecutar_agrupamiento_jerarquico("BD.csv")

    # Generar los dendrogramas en memoria
    def generate_dendrogram_base64(linkage_matrix,labels, title):
        plt.figure(figsize=(12, 6))
        plt.title(title)
        dendrogram(linkage_matrix, labels=labels, leaf_rotation=90)
        plt.xticks(rotation=90)
        plt.tight_layout()

        # Guardar la imagen en un buffer de memoria
        img_buffer = BytesIO()
        plt.savefig(img_buffer, format='PNG')
        plt.close()
        img_buffer.seek(0)

        # Codificar la imagen en base64
        img_base64 = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
        return img_base64

    # Generar imágenes con etiquetas
    ward_img_base64 = generate_dendrogram_base64(
        resultado["linkage_ward"],
        resultado["labels"],
        "Dendograma con método 'ward'"
    )
    average_img_base64 = generate_dendrogram_base64(
        resultado["linkage_average"],
        resultado["labels"],
        "Dendograma con método 'average'"
    )

    # Devolver respuesta
    return jsonify({
        "status": "success",
        "ward_score": resultado["ward_score"],
        "average_score": resultado["average_score"],
        "ward_img": f"data:image/png;base64,{ward_img_base64}",
        "average_img": f"data:image/png;base64,{average_img_base64}"
    })

    # Esta es otra version para cargar las imagenes
    # # Get the base URL dynamically
    # base_url = request.host_url  # e.g., "http://localhost:5000/"

    # return jsonify({
    #     "status": "success",
    #     "ward_score": resultado["ward_score"],
    #     "average_score": resultado["average_score"],
    #     "ward_img": f"/{resultado['ward_img']}",
    #     "average_img": f"/{resultado['average_img']}"
   



# Para pruebas locales, podemos usar el puerto estándar
if __name__ == '__main__':
    app.run(debug=True)
