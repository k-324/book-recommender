
import os
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

class get_similar_books:
    def __init__(self, csv_path="data/haodoo_books.csv", cache_dir="cache"):
        self.csv_path = csv_path
        self.cache_dir = cache_dir
        self.df = None
        self.vectorizer = TfidfVectorizer(stop_words="english")
        self.embeddings = None
        self._load_data()
        self._build_index()

    def _load_data(self):
        os.makedirs(self.cache_dir, exist_ok=True)
        self.df = pd.read_csv(self.csv_path)
        self.df = self.df.dropna(subset=["內容"])  # 避免空值影響向量化
        self.df["📚大綱"] = self.df["內容"].apply(self.extract_summary)
        self.df["📖分類"] = self.df["內容"].apply(self.extract_category)
        self.df["⭐評分"] = self.df["內容"].apply(lambda _: self.generate_stars())

    def _build_index(self):
        self.embeddings = self.vectorizer.fit_transform(self.df["內容"])
        # 儲存快取
        with open(os.path.join(self.cache_dir, "books.pkl"), "wb") as f:
            pickle.dump(self.df, f)
        np.save(os.path.join(self.cache_dir, "embeddings.npy"), self.embeddings.toarray())

    def extract_summary(self, text):
        return text.split("說明")[1].split("。")[0] if "說明" in text else text[:60]

    def extract_category(self, text):
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

    def generate_stars(self):
        return "⭐" * np.random.randint(3, 6)

    def search(self, query, top_k=5):
        query_vec = self.vectorizer.transform([query])
        cosine_sim = linear_kernel(query_vec, self.embeddings).flatten()
        top_indices = cosine_sim.argsort()[-top_k:][::-1]
        return self.df.iloc[top_indices]
