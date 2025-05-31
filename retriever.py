import os
import pickle
import numpy as np
import pandas as pd
import faiss
from sentence_transformers import SentenceTransformer

class get_similar_books:
    def __init__(self,
                 csv_path='data/haodoo_books.csv',
                 cache_dir='cache',
                 embedding_path='cache/embeddings.npy',
                 index_path='cache/faiss.index',
                 df_path='cache/books.pkl'):
        self.csv_path = csv_path
        self.cache_dir = cache_dir
        self.embedding_path = embedding_path
        self.index_path = index_path
        self.df_path = df_path

        self.model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
        self._load_or_build_index()

    def _load_data(self):
        os.makedirs(self.cache_dir, exist_ok=True)

        # 如果快取存在，直接讀取完整 dataframe
        if os.path.exists(self.df_path):
            with open(self.df_path, 'rb') as f:
                self.df = pickle.load(f)
        else:
            self.df = pd.read_csv(self.csv_path)
            self.df = self.df.dropna(subset=['內容'])

            def extract_summary(text):
                return text.split("說明")[1].split("。")[0] if "說明" in text else text[:60]

            def extract_category(text):
                if "科幻" in text: return "科幻"
                elif "愛情" in text: return "愛情"
                elif "哲學" in text: return "哲學"
                elif "成長" in text: return "成長"
                else: return "其他"

            def generate_stars():
                import random
                return "⭐" * random.randint(3, 5)

            self.df["大綱"] = self.df["內容"].apply(extract_summary)
            self.df["分類"] = self.df["內容"].apply(extract_category)
            self.df["評分"] = self.df["內容"].apply(lambda _: generate_stars())

            with open(self.df_path, 'wb') as f:
                pickle.dump(self.df, f)

    def _load_or_build_index(self):
        self._load_data()

        if os.path.exists(self.embedding_path) and os.path.exists(self.index_path):
            self.embeddings = np.load(self.embedding_path)
            self.index = faiss.read_index(self.index_path)
        else:
            self.embeddings = self.model.encode(self.df["內容"].tolist(), show_progress_bar=True)
            self.index = faiss.IndexFlatL2(self.embeddings.shape[1])
            self.index.add(self.embeddings)

            np.save(self.embedding_path, self.embeddings)
            faiss.write_index(self.index, self.index_path)

    def search(self, query, top_k=5):
        query_embedding = self.model.encode([query])
        _, indices = self.index.search(query_embedding, top_k)
        return self.df.iloc[indices[0]]
