import json
from ollama import Client

client = Client(host="http://localhost:11434")
sentences = ["The Earth orbits the Sun.", "However, some people claim the Moon is made of cheese."]
prompt = f"""
You are an expert fact-checker assistant. Your task is to identify which sentences contain verifiable factual claims.
A verifiable factual claim is a statement that can be proven true or false using objective evidence.

Return ONLY a JSON object with a single key "claims" containing an array of strings representing the verifiable claims.

Sentences:
{json.dumps(sentences)}
"""

print("Sending prompt to Ollama...")
response = client.generate(model="qwen2.5:7b", prompt=prompt, format="json")
print("Response:", repr(response["response"]))
