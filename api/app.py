# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS

import torch
from sentence_transformers import SentenceTransformer

import pandas as pd
import os
import numpy as np

from hnsw_manager import HNSWIndexManager
from utils import set_seed, process_text

app = Flask(__name__)
CORS(app)

set_seed()

base_dir = os.path.dirname(os.path.abspath(__file__))
data_path = os.path.join(base_dir, "data", "data.xlsx")
embeddings_path = os.path.join(base_dir, "embeddings", "embeddings.npy")

data = pd.read_excel(data_path)
embeddings = np.load(embeddings_path)

model = SentenceTransformer("multi-qa-mpnet-base-dot-v1")
device = "cuda" if torch.cuda.is_available() else "cpu"
model = model.to(device)

hnsw_manager = HNSWIndexManager(embeddings)


@app.route("/similar-articles", methods=["POST"])
def recommend():
    content = request.get_json(silent=True)
    if not content or "query" not in content:
        return jsonify({"error": "Query input is required!"}), 400

    q_input = content["query"]
    max_results = request.args.get("maxResults", default=3, type=int)
    if max_results > 4:
        return jsonify({"error": "Max results should not exceed 4!"}), 400

    processed_query = process_text(q_input)
    query_embedding = model.encode([processed_query])[0]
    ids, distances = hnsw_manager.query(query_embedding, k=max_results)

    best_fits = []
    for i, dist in zip(ids[0], distances[0]):
        best_fits.append(
            {
                "id": int(i),
                "title": data["Title"].values[i],
                "label": data["Label"].values[i],
                "text": data["Text"].values[i],
                "url": data["URL"].values[i],
                "distance": float(dist),
            }
        )

    return jsonify(best_fits)


if __name__ == "__main__":
    app.run(debug=True)
