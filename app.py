import streamlit as st
from retriever import get_similar_books
from generator import generate_recommendation
from main import recommend_books

retriever = get_similar_books()
generator = generate_recommendation(model_name='taide-lx-7b-chat-4bit')
