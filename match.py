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
        combined_text = f"{item['Response']} {item['Bio']}"
        collection.add(
            documents=[combined_text],
            metadatas=[{
                "name": item['Name'],
                "availability": item['Availability']
            }],
            ids=[item['Phone']]
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

def map_ids_to_phone_numbers(matches: List[Tuple[int, int]], ids: List[str]) -> List[Tuple[str, str]]:
    return [(ids[i], ids[j]) for i, j in matches]

def print_matches(matched_phone_numbers: List[Tuple[str, str]]):
    for i, (phone1, phone2) in enumerate(matched_phone_numbers, 1):
        print(f"Match {i}: {phone1} - {phone2}")

def predictPair(data):
    # Load and process data
    add_documents_to_collection(data)

    # Generate distance matrix
    distance_matrix, ids = generate_distance_matrix(collection)

    # Apply Best-First Greedy algorithm
    matches = best_first_greedy_matching(distance_matrix)

    # Map matches to phone numbers
    matched_phone_numbers = map_ids_to_phone_numbers(matches, ids)

    # Print results
    print_matches(matched_phone_numbers)


    return matched_phone_numbers
