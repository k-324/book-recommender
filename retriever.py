import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import pickle
from pathlib import Path
import random


class get_similar_books:
    def __init__(
        self,
        csv_path=Path(__file__).parent / "data" / "haodoo_books.csv",
        cache_dir="cache",
        embedding_model_name="intfloat/multilingual-e5-large"
    ):
        self.csv_path = csv_path
        self.cache_dir = cache_dir
        self.embedding_path = os.path.join(cache_dir, "embeddings.npy")
        self.index_path = os.path.join(cache_dir, "faiss.index")
        self.df_path = os.path.join(cache_dir, "books.pkl")
        self.model = SentenceTransformer(embedding_model_name)
        self.dimension = self.model.get_sentence_embedding_dimension()

        self._load_data()
        self._load_or_build_index()

    def _load_data(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        if os.path.exists(self.df_path):
            with open(self.df_path, "rb") as f:
                self.df = pickle.load(f)
        else:
            self.df = pd.read_csv(self.csv_path)
            self.df = self.df.dropna(subset=["內容"])

            # 加入大綱提取與分類欄位
            def extract_summary(text):
                return text.split("說明")[1].split()[0] if "說明" in text else text[:60]

            def extract_category(text):
                if "科幻" in text:
                    return "科幻"
                elif "愛情" in text:
                    return "愛情"
                elif "哲學" in text:
                    return "哲學"
                elif "成長" in text:
                    return "成長"
                else:
                    return "其他"

            def generate_stars():
                return "⭐️" * random.randint(3, 5)

            self.df["大綱"] = self.df["內容"].apply(extract_summary)
            self.df["分類"] = self.df["內容"].apply(extract_category)
            self.df["評分"] = self.df["內容"].apply(lambda _: generate_stars())

            with open(self.df_path, "wb") as f:
                pickle.dump(self.df, f)

    def _load_or_build_index(self):
        if os.path.exists(self.embedding_path) and os.path.exists(self.index_path):
            print("已載入快取的embeddings與FAISS index。")
            self.embeddings = np.load(self.embedding_path)
            self.index = faiss.read_index(self.index_path)
        else:
            print("建立embedding與FAISS index中...")
            self.embeddings = self._embed_texts(self.df["內容"].tolist())
            np.save(self.embedding_path, self.embeddings)
            self.index = faiss.IndexFlatL2(self.dimension)
            self.index.add(self.embeddings)
            faiss.write_index(self.index, self.index_path)
            print("已完成儲存 embeddings 與 index。")

    def _embed_texts(self, texts):
        return self.model.encode(
            ["query: " + text for text in texts],
            show_progress_bar=True,
            convert_to_numpy=True,
            normalize_embeddings=True
        )

    def search(self, query, top_k=5):
        query_embedding = self._embed_texts([query])
        distances, indices = self.index.search(query_embedding, top_k)
        results = self.df.iloc[indices[0]].copy()
        results["score"] = distances[0]
        return results
