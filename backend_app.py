from flask import Flask, request, jsonify
import os
import openai
import json
from utils.embeddings import create_embedding, search_embeddings

app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("Warning: OPENAI_API_KEY not set. Set it from .env or environment before running.")
openai.api_key = OPENAI_API_KEY

# ChromaDB data path
CHROMA_PATH = os.path.join(os.path.dirname(__file__), "data", "sample_chroma.json")

def load_chroma():
    if os.path.exists(CHROMA_PATH):
        with open(CHROMA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_chroma(data):
    os.makedirs(os.path.dirname(CHROMA_PATH), exist_ok=True)
    with open(CHROMA_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

chroma_data = load_chroma()

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

@app.route('/index', methods=['POST'])
def index_repo():
    files = request.json.get('files', {})
    for path, text in files.items():
        emb = create_embedding(text)
        chroma_data.append({"id": path, "text": text, "embedding": emb})
    save_chroma(chroma_data)
    return jsonify({"indexed_files": len(files), "message": "ChromaDB updated with new entries"})

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json or {}
    prompt = data.get("prompt", "")
    # Retrieve top 3 relevant chunks
    context_chunks = search_embeddings(chroma_data, prompt, top_k=3)
    system_msg = "You are a helpful AI coding assistant. Use the following context from the repository:\n"
    context_msg = "\n".join([c['text'] for c in context_chunks])
    messages = [
        {"role": "system", "content": system_msg + context_msg},
        {"role": "user", "content": prompt}
    ]
    try:
        resp = openai.ChatCompletion.create(
            model="gpt-4-mini",
            messages=messages,
            max_tokens=512,
            temperature=0.2
        )
        reply = resp['choices'][0]['message']['content']
    except Exception as e:
        reply = f"[error calling OpenAI API: {e}]"
    return jsonify({"reply": reply})

@app.route('/on_push', methods=['POST'])
def on_push():
    payload = request.json or {}
    ref = payload.get("ref", "unknown")
    review = f"Assistant review for push {ref}: Looks good. (GPT-4-mini mock review)"
    return jsonify({"review": review})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=True)
