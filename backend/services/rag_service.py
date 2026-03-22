# temporary dataset
DATA = [
    "Interstellar - Sci-fi movie about space and time",
    "Inception - Mind-bending thriller",
    "The Matrix - Virtual reality sci-fi",
    "The Notebook - Romantic drama",
]

def process_query(query):
    results = []

    for item in DATA:
        if query.lower() in item.lower():
            results.append(item)

    if not results:
        return "No results found"

    return results