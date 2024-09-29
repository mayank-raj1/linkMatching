import json
import chromadb
from chromadb.utils import embedding_functions
import numpy as np
from typing import List, Tuple

# Initialize the ChromaDB client
client = chromadb.Client()

# Create a sentence transformer embedding function
sentence_transformer_ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

# Create a collection with the specified embedding function
collection = client.create_collection("matchmaking_collection", embedding_function=sentence_transformer_ef)

def load_json_data(file_path: str) -> List[dict]:
    with open(file_path, 'r') as jsonfile:
        return json.load(jsonfile)

def add_documents_to_collection(data: List[dict]):
    for item in data:
        collection.add(
            documents=[item['Bio+Response']],
            metadatas=[{"id": item['ID'], "phone": item['Phone Number']}],
            ids=[item['ID']]
        )

def generate_distance_matrix(collection) -> Tuple[np.ndarray, List[str]]:
    results = collection.get()
    documents = results['documents']
    ids = results['ids']

    n = len(documents)
    distance_matrix = np.zeros((n, n))

    for i in range(n):
        query_results = collection.query(
            query_texts=[documents[i]],
            n_results=n
        )
        distances = query_results['distances'][0]
        
        for j, doc_id in enumerate(query_results['ids'][0]):
            idx = ids.index(doc_id)
            distance_matrix[i, idx] = distances[j]

    return distance_matrix, ids

def best_first_greedy_matching(distances: np.ndarray) -> List[Tuple[int, int]]:
    n = len(distances)
    unmatched = set(range(n))
    matches = []

    all_pairs = [(i, j, distances[i][j]) 
                 for i in range(n) 
                 for j in range(i+1, n)]
    
    all_pairs.sort(key=lambda x: x[2])

    for i, j, _ in all_pairs:
        if i in unmatched and j in unmatched:
            matches.append((i, j))
            unmatched.remove(i)
            unmatched.remove(j)
        
        if not unmatched:  # All participants are matched
            break

    return matches

def map_ids_to_documents(matches: List[Tuple[int, int]], ids: List[str], data: List[dict]) -> List[Tuple[dict, dict]]:
    id_to_doc = {item['ID']: item for item in data}
    return [(id_to_doc[ids[i]], id_to_doc[ids[j]]) for i, j in matches]

def print_matches(matched_documents: List[Tuple[dict, dict]]):
    for i, (doc1, doc2) in enumerate(matched_documents, 1):
        print(f"\nMatch {i}:")
        print(f"Person 1 (ID: {doc1['ID']}, Phone: {doc1['Phone Number']}):")
        print(f"  {doc1['Bio+Response']}")
        print(f"Person 2 (ID: {doc2['ID']}, Phone: {doc2['Phone Number']}):")
        print(f"  {doc2['Bio+Response']}")

def main():
    # Load and process data
    data = load_json_data('/Users/jibk/Desktop/wtf/maybeeeeeee/data.json')
    add_documents_to_collection(data)

    # Generate distance matrix
    distance_matrix, ids = generate_distance_matrix(collection)

    # Apply Best-First Greedy algorithm
    matches = best_first_greedy_matching(distance_matrix)

    # Map matches back to original documents
    matched_documents = map_ids_to_documents(matches, ids, data)

    # Print results
    print_matches(matched_documents)

if __name__ == "__main__":
    main()