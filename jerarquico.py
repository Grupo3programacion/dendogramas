import os
import uuid
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
from sklearn.utils import resample
from scipy.cluster.hierarchy import linkage, dendrogram, fcluster
import matplotlib.pyplot as plt

# def ejecutar_agrupamiento_jerarquico(csv_path, n_clusters=4):
#     df = pd.read_csv(csv_path)

#     # Filtrar solo las filas que tienen abstract
#     df_clean = df.dropna(subset=["abstract"]).copy()
#     abstracts = df_clean["abstract"]

#     vectorizer = TfidfVectorizer(stop_words="english")
#     tfidf_matrix = vectorizer.fit_transform(abstracts)
#     tfidf_dense = tfidf_matrix.toarray()

#     # Crear una muestra si hay más de 100 elementos
#     if len(tfidf_dense) > 100:
#         df_clean["v"] = tfidf_dense.tolist()
#         sample_df = resample(df_clean[["titulo", "abstract", "v"]], n_samples=100, random_state=42)
#         tfidf_dense_sampled = sample_df["v"].tolist()
#         labels = sample_df["titulo"].fillna(sample_df["abstract"].str[:30] + "...").tolist()
#     else:
#         tfidf_dense_sampled = tfidf_dense
#         labels = df_clean["titulo"].fillna(df_clean["abstract"].str[:30] + "...").tolist()

#     # Crear linkage
#     linkage_ward = linkage(tfidf_dense_sampled, method="ward")
#     linkage_average = linkage(tfidf_dense_sampled, method="average", metric="cosine")

#     # Crear carpeta para guardar imágenes
#     output_dir = os.path.join("static", "images")
#     os.makedirs(output_dir, exist_ok=True)

#     # Nombres de los archivos de imagen
#     ward_filename = f"ward_dendograma_{uuid.uuid4().hex[:8]}.png"
#     average_filename = f"average_dendograma_{uuid.uuid4().hex[:8]}.png"

#     ward_path = os.path.join(output_dir, ward_filename)
#     average_path = os.path.join(output_dir, average_filename)

#     # Dendrograma - Ward
#     plt.figure(figsize=(12, 6))
#     plt.title("Dendograma con método 'ward'")
#     dendrogram(linkage_ward, labels=labels, truncate_mode="level", p=20)
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(ward_path, bbox_inches='tight')
#     plt.close()

#     # Dendrograma - Average
#     plt.figure(figsize=(12, 6))
#     plt.title("Dendograma con método 'average'")
#     dendrogram(linkage_average, labels=labels, truncate_mode="level", p=20)
#     plt.xticks(rotation=90)
#     plt.tight_layout()
#     plt.savefig(average_path, bbox_inches='tight')
#     plt.close()

#     # Evaluar agrupamiento original completo
#     labels_ward = fcluster(linkage(tfidf_dense, method="ward"), t=n_clusters, criterion='maxclust')
#     labels_avg = fcluster(linkage(tfidf_dense, method="average", metric="cosine"), t=n_clusters, criterion='maxclust')

#     score_ward = silhouette_score(tfidf_matrix, labels_ward, metric="cosine")
#     score_avg = silhouette_score(tfidf_matrix, labels_avg, metric="cosine")

#     print(f"Silhouette Score - Ward: {score_ward:.4f}")
#     print(f"Silhouette Score - Average: {score_avg:.4f}")

#     return {
#         "ward_score": score_ward,
#         "average_score": score_avg,
#         "ward_img": f"/static/images/{ward_filename}",
#         "average_img": f"/static/images/{average_filename}"
#     }


def ejecutar_agrupamiento_jerarquico(csv_path, n_clusters=4):
    df = pd.read_csv(csv_path)

    # Filtrar solo las filas que tienen abstract
    df_clean = df.dropna(subset=["abstract"]).copy()
    abstracts = df_clean["abstract"]

    vectorizer = TfidfVectorizer(stop_words="english")
    tfidf_matrix = vectorizer.fit_transform(abstracts)
    tfidf_dense = tfidf_matrix.toarray()

    # Crear una muestra si hay más de 20 elementos
    if len(tfidf_dense) > 100:
        df_clean["v"] = tfidf_dense.tolist()
        sample_df = resample(df_clean[["titulo", "abstract", "v"]], n_samples=20, random_state=42)
        tfidf_dense_sampled = sample_df["v"].tolist()
        labels = sample_df["titulo"].fillna(sample_df["abstract"].str[:30] + "...").tolist()
    else:
        tfidf_dense_sampled = tfidf_dense
        labels = df_clean["titulo"].fillna(df_clean["abstract"].str[:30] + "...").tolist()

    # Crear linkage
    linkage_ward = linkage(tfidf_dense_sampled, method="ward")
    linkage_average = linkage(tfidf_dense_sampled, method="average", metric="cosine")

    # Evaluar agrupamiento original completo
    labels_ward = fcluster(linkage(tfidf_dense, method="ward"), t=n_clusters, criterion='maxclust')
    labels_avg = fcluster(linkage(tfidf_dense, method="average", metric="cosine"), t=n_clusters, criterion='maxclust')

    score_ward = silhouette_score(tfidf_matrix, labels_ward, metric="cosine")
    score_avg = silhouette_score(tfidf_matrix, labels_avg, metric="cosine")

    print(f"Silhouette Score - Ward: {score_ward:.4f}")
    print(f"Silhouette Score - Average: {score_avg:.4f}")

    return {
        "ward_score": score_ward,
        "average_score": score_avg,
        "linkage_ward": linkage_ward,
        "linkage_average": linkage_average,
        "labels": labels
    }