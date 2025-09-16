from openai import OpenAI
import faiss
import numpy as np

# 1. Get embeddings from OpenAI
client = OpenAI()

texts = ["dog", "puppy", "car"]
embeddings = [client.embeddings.create(model="text-embedding-3-small", input=t).data[0].embedding for t in texts]

# 2. Store in FAISS (vector database)
dimension = len(embeddings[0])
index = faiss.IndexFlatL2(dimension) # L2 = Euclidean distance
index.add(np.array(embeddings, dtype="float32")) # type: ignore

# 3. Query search
query = "cute puppy"
query_embedding = client.embeddings.create(model="text-embedding-3-small", input=query).data[0].embedding
D, I = index.search(np.array([query_embedding]), k=2)  # type: ignore # find top-2 matches

print("Query:", query)
print("Closest matches:", [texts[i] for i in I[0]])