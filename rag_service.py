import os
import json

class RAGService:
    def __init__(self):
        self.knowledge_base_path = "data/knowledge.json"
        self.load_knowledge()

    def load_knowledge(self):
        if os.path.exists(self.knowledge_base_path):
            with open(self.knowledge_base_path, 'r') as f:
                self.data = json.load(f)
        else:
            self.data = [
                {"text": "KAIN stands for Knowledge Augmented Intelligent Network.", "category": "general"},
                {"text": "KAIN was built using FastAPI and React.", "category": "tech"},
                {"text": "KAIN uses Gemini 1.5 Flash for its LLM capabilities.", "category": "tech"}
            ]
            # Create the data directory and save initial knowledge
            os.makedirs("data", exist_ok=True)
            with open(self.knowledge_base_path, 'w') as f:
                json.dump(self.data, f)

    def search(self, query, top_k=3):
        # A simple keyword-based search as a placeholder for a Vector DB like FAISS/Pinecone
        # In a real scenario, we would use embeddings and cosine similarity
        results = []
        query_words = query.lower().split()
        
        for item in self.data:
            score = 0
            for word in query_words:
                if word in item['text'].lower():
                    score += 1
            if score > 0:
                results.append((item['text'], score))
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x[1], reverse=True)
        return "\n".join([r[0] for r in results[:top_k]])

rag_service = RAGService()
