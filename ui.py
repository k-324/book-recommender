import streamlit as st
from main import recommend_books
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