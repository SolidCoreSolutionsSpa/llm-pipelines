from app.core.openai_client import OpenAIClient

class OpenAIModel:
    def __init__(self):
        self.client = OpenAIClient()

    def generate_text(self, prompt: str, max_tokens: int = 50):
        response = self.client.generate_text(prompt, max_tokens)
        return response
