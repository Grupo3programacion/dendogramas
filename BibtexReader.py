import bibtexparser

class BibtexReader:
    def __init__(self, filepath):
        """
        Inicializa el lector de BibTeX con la ruta del archivo.

        :param filepath: Ruta del archivo .bib a procesar.
        """
        self.filepath = filepath
        self.entries = []  # Almacena las entradas cargadas desde el archivo

    def load_entries(self):
        """
        Carga y parsea el archivo BibTeX, almacenando las entradas en self.entries.

        :return: Una lista de diccionarios, cada uno representando una entrada en el archivo BibTeX.
        """
        try:
            with open(self.filepath, encoding="utf-8") as bibtex_file:
                bib_database = bibtexparser.load(bibtex_file)
                self.entries = bib_database.entries
            return self.entries
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return []

    def filter_entries(self, field, value):
        """
        Filtra las entradas según un campo específico y un valor dado.

        :param field: Campo a evaluar (por ejemplo, "year", "author", "keywords").
        :param value: Valor a buscar en el campo especificado.
        :return: Lista de entradas que cumplen con el criterio.
        """
        if not self.entries:
            print("No hay entradas cargadas. Carga las entradas primero con load_entries.")
            return []

        # Filtra las entradas con el campo y valor especificados
        filtered_entries = [entry for entry in self.entries if field in entry and value in entry[field]]
        return filtered_entries

    def get_unique_values(self, field):
        """
        Obtiene una lista de valores únicos en un campo específico de las entradas cargadas.

        :param field: Campo en el cual buscar valores únicos (por ejemplo, "year" o "journal").
        :return: Lista de valores únicos en el campo.
        """
        if not self.entries:
            print("No hay entradas cargadas. Carga las entradas primero con load_entries.")
            return []

        # Extrae valores únicos del campo especificado
        unique_values = set(entry[field] for entry in self.entries if field in entry)
        return list(unique_values)

    def get_entry_by_id(self, entry_id):
        """
        Busca una entrada específica por su ID único.

        :param entry_id: ID de la entrada (clave única del artículo en el archivo).
        :return: Diccionario con la entrada encontrada, o None si no existe.
        """
        for entry in self.entries:
            if entry.get("ID") == entry_id:
                return entry
        print(f"Entrada con ID {entry_id} no encontrada.")
        return None

    def count_entries(self):
        """
        Devuelve el número total de entradas cargadas en el archivo BibTeX.

        :return: Número de entradas en el archivo.
        """
        return len(self.entries)

    def get_abstracts(self):
        """
        Extrae los abstracts de las entradas cargadas.

        :return: Lista de abstracts de las entradas.
        """
        if not self.entries:
            print("No hay entradas cargadas. Carga las entradas primero con load_entries.")
            return []

        abstracts = [entry.get("abstract", "") for entry in self.entries if "abstract" in entry]
        return abstracts