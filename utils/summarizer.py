# 📄 utils/summarizer.py
import re
import heapq
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np

def extract_summary(text, n=3):
    sentences = re.split(r'(?<=[。！？])', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
    vectorizer = CountVectorizer().fit_transform(sentences)
    vectors = vectorizer.toarray()
    scores = np.sum(vectors, axis=1)
    top_n = heapq.nlargest(n, zip(scores, sentences))
    return [s for _, s in top_n]
