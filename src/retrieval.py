import pandas as pd
import chromadb
from sentence_transformers import SentenceTransformer
import os

# Initialize global components
model = SentenceTransformer('all-MiniLM-L6-v2')
client = chromadb.Client()
collection = client.get_or_create_collection(name="facts")

def index_facts(csv_path="data/facts.csv"):
    """
    Reads facts from CSV and indexes them in ChromaDB.
    """
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return

    df = pd.read_csv(csv_path)
    
    ids = [str(x) for x in df['id'].tolist()]
    documents = df['text'].tolist()
    metadatas = df[['source', 'date']].to_dict('records')
    
    # Check if already indexed (naive check)
    if collection.count() == 0:
        print("Indexing facts...")
        embeddings = model.encode(documents)
        collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas
        )
        print(f"Indexed {len(documents)} facts.")
    else:
        print("Facts already indexed.")

def retrieve_facts(query, k=3):
    """
    Retrieves the top-k most similar facts for a given query.
    """
    results = collection.query(
        query_embeddings=model.encode([query]),
        n_results=k
    )
    
    retrieved = []
    if results['documents']:
        for i in range(len(results['documents'][0])):
            retrieved.append({
                "text": results['documents'][0][i],
                "source": results['metadatas'][0][i]['source'],
                "date": results['metadatas'][0][i]['date'],
                "distance": results['distances'][0][i] if 'distances' in results else None
            })
            
    return retrieved

if __name__ == "__main__":
    # Test
    index_facts()
    query = "free electricity for farmers"
    results = retrieve_facts(query)
    for r in results:
        print(r)
