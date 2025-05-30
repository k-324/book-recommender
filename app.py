import streamlit as st
from retriever import get_similar_books
import openai
import pandas as pd

# 請確保你有設置 OpenAI API 金鑰
openai.api_key = st.secrets["OPENAI_API_KEY"]

# 使用 GPT 生成內容摘要大綱
def generate_outline(content):
    if not content or len(content) < 50:
        return ["內容過少，無法產生重點摘要。"]
    try:
        prompt = f"請將以下書籍內容整理成 3-5 點精選重點，每點一句話：\n\n{content}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        raw = response["choices"][0]["message"]["content"]
        return [line.strip("-•● 。") for line in raw.split("\n") if line.strip()]
    except Exception as e:
        return [f"⚠️ 無法產生摘要：{e}"]

# Streamlit 設定
st.set_page_config(page_title="Book一試", page_icon="📘", layout="centered")

st.markdown("""
    <h1 style='text-align: center; color: #4B3832;'>📘 Book一試</h1>
    <p style='text-align: center; color: #6E6658;'>一個溫暖又極簡的書籍推薦系統，從浩瀚書海中找到你的下一本最愛。</p>
""", unsafe_allow_html=True)

st.markdown("---")

# 使用者輸入
user_input = st.text_input("請輸入你喜歡的主題或關鍵字：", placeholder="例如：哲學、成長、愛情、科幻…")

# 推薦書籍
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
                    
                    # 分類與星級評分
                    st.markdown(f"📚 分類： {book['📖分類']}")
                    st.markdown(f"⭐ 評分：{book['⭐評分']}")
                    
                    # 大綱與完整內容
                    if pd.notna(book["內容"]) and len(book["內容"]) > 30:
                        with st.expander("📖 精選重點："):
                            outline = generate_outline(book["內容"])
                            for point in outline:
                                st.markdown(f"- {point}")
                    else:
                        st.markdown("📖 尚無可顯示內容。")

                    st.markdown("---")
        else:
            st.warning("目前找不到符合的書籍，請換個關鍵字試試看！")
    else:
        st.info("請先輸入一些想看的主題或關鍵字喔！")
