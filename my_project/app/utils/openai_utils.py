import openai
import json
import numpy as np
import requests
from app.config import settings
from app.core.config.logger import logger

openai.api_key = settings.OPENAI_API_KEY
EMBEDDING_ENDPOINT = "https://api.openai.com/v1/embeddings"

class EmbeddingManager:
    def __init__(self, model="text-embedding-ada-002"):
        self.model = model

    def get_embedding(self, text):
        headers = {
            "Authorization": f"Bearer {openai.api_key}",
            "Content-Type": "application/json"
        }
        response = requests.post(
            EMBEDDING_ENDPOINT,
            headers=headers,
            json={
                "model": self.model,
                "input": text
            }
        )
        response_data = response.json()
        if 'data' in response_data:
            return response_data['data'][0]['embedding']
        else:
            logger.info(f"Error en la respuesta de embeddings: {response_data}")
            raise ValueError(f"Error en la respuesta de embeddings: {response_data}")

    def get_entities_embeddings(self, entities):
        embeddings = {}
        for entity in entities:
            embeddings[entity['id']] = self.get_embedding(entity['text'])
        return embeddings

    def cosine_similarity(self, vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    def match_entities(self, query_entities, entity_embeddings, min_similarity=0.8):
        query_embeddings = {entity['text']: self.get_embedding(entity['text']) for entity in query_entities}
        
        matching_entities = []
        for query, query_embedding in query_embeddings.items():
            similarities = {entity_id: self.cosine_similarity(query_embedding, entity_embedding) 
                            for entity_id, entity_embedding in entity_embeddings.items()}
            
            matching = sorted(
                [(entity_id, similarity) for entity_id, similarity in similarities.items() if similarity >= min_similarity],
                key=lambda item: item[1],
                reverse=True
            )
            
            top_matching = [entity_id for entity_id, similarity in matching[:3]]

            logger.info(f"Consulta: {query}, Entidades coincidentes: {top_matching}")
            
            if top_matching:
                matching_entities.append(top_matching)
            else:
                matching_entities.append(None)
        
        return matching_entities

    def process_and_save_embeddings(self, input_file, output_file):
        entities = self.load_entities(input_file)
        entity_embeddings = self.get_entities_embeddings(entities)
        self.save_embeddings(entity_embeddings, output_file)
        return {"message": f"Embeddings saved to {output_file}"}

    def load_entities(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            entities = json.load(file)
        return entities

    def save_embeddings(self, embeddings, file_path):
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(embeddings, file, ensure_ascii=False, indent=4)