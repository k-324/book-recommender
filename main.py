import streamlit as st
from retriever import get_similar_books
from generator import generate_recommendation
import concurrent.futures
def recommend_books(user_input, top_k=3):
    retriever = get_similar_books()
    generator = generate_recommendation()
    similar_books = retriever.search(user_input, top_k=top_k)
    def generate_for_book(book):
        title = getattr(book, "書名", getattr(book, "title", ""))
        content = getattr(book, "內容", getattr(book, "content", ""))
        author = getattr(book, "作者", getattr(book, "author", ""))
        reason = generator.generate_reason(user_input, title, content)
        return {
            "title": title,
            "author": author,
            "reason": reason
        }
    with concurrent.futures.ThreadPoolExecutor() as executor:
        recommendations = list(executor.map(generate_for_book, similar_books.itertuples()))
    
    return recommendations
st.set_page_config(page_title="書籍推薦小幫手")
st.title("📚 書籍推薦小幫手")
st.markdown("請輸入你的閱讀需求，讓我們推薦符合你心情或興趣的書籍！")
user_input = st.text_area("📝 你有什麼樣的需求呢？", placeholder="例如：我最近壓力很大，想找些療癒系的書...")
if st.button("推薦給我"):
    if not user_input.strip():
        st.warning("請輸入一些內容喔！")
    else:
        with st.spinner("系統思考中..."):
            results = recommend_books(user_input)
        st.success("這是我們為你推薦的書：")
        for book in results:
            st.markdown("---")
            st.markdown(f"### 《{book['title']}》by {book['author']}")
            st.markdown(f"📘 **推薦理由：** {book['reason']}")