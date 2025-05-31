# app.py
import streamlit as st
from retriever import get_similar_books

st.set_page_config(page_title="Book一試", page_icon="📘", layout="centered")
st.markdown("""
    <h1 style='text-align: center; color: #4B3832;'>📘 Book一試</h1>
    <p style='text-align: center; color: #6E6658;'>一個溫暖又極簡的書籍推薦系統，從浩瀚書海中找到你的下一本最愛。</p>
""", unsafe_allow_html=True)

st.markdown("---")

user_input = st.text_input("請輸入你喜歡的主題或關鍵字：", placeholder="例如：哲學、成長、愛情、科幻…")

if st.button("📚 給我推薦！"):
    if user_input.strip():
        with st.spinner("正在為你尋找書籍中..."):
            recommender = get_similar_books()
            recommendations = recommender.search(user_input)

        if not recommendations.empty:
            st.success(f"找到 {len(recommendations)} 本好書：")
            for _, book in recommendations.iterrows():
                with st.container():
                    st.markdown(f"### {book['書名']}")
                    st.markdown(f"**作者：** {book['作者']}")
                    st.markdown(f"📚 **分類：** {book['分類']}  |  ⭐️ **評分：** {book.get('星級評分', '尚無評分')}")
                    st.markdown("**📖 精選重點：**")
                    for point in book['簡介重點']:
                        st.markdown(f"- {point}")
                    st.markdown(f"🗓️ **出版年份：** {'、'.join(book['出版年份'])}")

                    if st.button("🔎 查看完整內容", key=book['書名']):
                        st.switch_page(f"/pages/{book['書名'].replace(' ', '_')}.py")

                    st.markdown("---")
        else:
            st.warning("目前找不到符合的書籍，請換個關鍵字試試看！")
    else:
        st.info("請先輸入一些想看的主題或關鍵字喔！")
