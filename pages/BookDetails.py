# 📄 pages/BookDetails.py
import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    df = pd.read_csv("haodoo_books.csv")
    df = df[df["是否成功擷取內容"] == True].copy()
    df.dropna(subset=["內容"], inplace=True)
    return df

df = load_data()
params = st.experimental_get_query_params()
book_title = params.get("book", [None])[0]

if book_title:
    book = df[df["書名"] == book_title].iloc[0]
    st.title(f"📘《{book['書名']}》")
    st.markdown(f"✍️ 作者：{book['作者']}")
    st.markdown(f"🏷️ 分類：{book['分類']}")
    st.markdown(f"⭐ 評分：4.3（模擬）")
    st.markdown("📖 **完整內容：**")
    st.markdown(book["內容"])
    st.markdown(f"[🔗 原始頁面連結]({book['網址']})")
else:
    st.warning("未指定書籍標題，請從主頁點選連結。")
