import streamlit as st
from retriever import get_similar_books

# 頁面設定：標題、icon、置中顯示
st.set_page_config(page_title="Book一試", page_icon="📘", layout="centered")

# 美化主標題與說明
st.markdown("""
    <h1 style='text-align: center; color: #4B3832;'>📘 Book一試</h1>
    <p style='text-align: center; color: #6E6658;'>一個溫暖又簡易的書籍推薦系統，從浩瀚書海中找到你的下一本最愛。</p>
""", unsafe_allow_html=True)

st.markdown("---")

# 使用者輸入需求
user_input = st.text_input("📖 你有什麼樣的需求呢？", placeholder="例如：我最近壓力很大，想找些療癒系的書…")

# 點擊按鈕開始推薦
if st.button("📚 一鍵推推！"):
    if user_input.strip():
        with st.spinner("書海遨遊中..."):
            recommendations = get_similar_books(user_input)

        if recommendations:
            st.success(f"找到 {len(recommendations)} 本書籍：")
            for book in recommendations:
                with st.container():
                    st.markdown(f"### 📘 {book['title']}")
                    st.markdown(f"👤 **作者：** {book['author']}")
                    st.markdown(f"📝 {book['summary'][:120]}...")
                    st.markdown("---")
        else:
            st.warning("目前找不到符合的書籍，請換個關鍵字試試看！")
    else:
        st.info("請先輸入一些想看的主題或需求喔！")
