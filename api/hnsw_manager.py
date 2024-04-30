import hnswlib


class HNSWIndexManager:
    def __init__(self, embeddings, space="cosine", dim=None, ef_construction=200, M=16):
        self.dim = dim if dim else embeddings.shape[1]
        self.index = hnswlib.Index(space=space, dim=self.dim)
        self.index.init_index(
            max_elements=len(embeddings), ef_construction=ef_construction, M=M
        )
        self.index.add_items(embeddings)
        self.index.set_ef(50)

    def query(self, query_embedding, k):
        return self.index.knn_query(query_embedding, k)
