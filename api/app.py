from flask import Flask, request, jsonify
from flask_cors import CORS

from sklearn.neighbors import NearestNeighbors
from sentence_transformers import SentenceTransformer

import numpy as np
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

base_dir = os.path.dirname(os.path.abspath(__file__))

data_path = os.path.join(base_dir, "data", "wiki_train.xlsx")
embeddings_path = os.path.join(base_dir, "embeddings", "wiki_train_embeddings.npy")

data = pd.read_excel(data_path)
embeddings = np.load(embeddings_path)

model = SentenceTransformer("all-mpnet-base-v2")

nn_model = NearestNeighbors(n_neighbors=5, algorithm="auto", metric="cosine")
nn_model.fit(embeddings)


@app.route("/recommend", methods=["POST"])
def recommend():
    content = request.get_json(silent=True)
    if not content or "query" not in content:
        return jsonify({"error": "Query input is required!"}), 400

    q_input = content["query"]
    max_results = request.args.get("maxResults", default=3, type=int)
    if max_results > 4:
        return jsonify({"error": "Max results should not exceed 4!"}), 400

    query_embedding = model.encode([q_input], convert_to_tensor=False)
    query_embedding = query_embedding.reshape(1, -1)

    distances, indices = nn_model.kneighbors(query_embedding, n_neighbors=max_results)

    best_fits = []
    for index, distance in zip(indices[0], distances[0]):
        best_fits.append(
            {
                "id": int(index),
                "title": data["Title"].iloc[index],
                "label": data["label"].iloc[index],
                "text": data["text"].iloc[index],
                "url": data["URL"].iloc[index],
                "distance": float(distance),
            }
        )

    return jsonify(best_fits)


if __name__ == "__main__":
    app.run(debug=True)
