# 📄 app.py
import streamlit as st
import pandas as pd
from utils.summarizer import extract_summary

@st.cache_data
def load_data():
    df = pd.read_csv("haodoo_books.csv")
    df = df[df["是否成功擷取內容"] == True].copy()
    df.dropna(subset=["內容"], inplace=True)
    df["條列簡介"] = df["內容"].apply(lambda x: extract_summary(x))
    return df

df = load_data()

st.set_page_config(page_title="書籍推薦系統", layout="wide")
st.title("📚 書籍推薦系統")

keyword = st.text_input("輸入你想找的書籍主題、關鍵字：")

if keyword:
    result_df = df[df["內容"].str.contains(keyword, case=False)]
else:
    result_df = df.sample(10)

st.write(f"共找到 {len(result_df)} 本書：")

for i, row in result_df.iterrows():
    st.markdown("---")
    cols = st.columns([2, 1])
    with cols[0]:
        st.subheader(f"📘《{row['書名']}》")
        st.markdown(f"✍️ 作者：{row['作者']}  ")
        st.markdown(f"🏷️ 分類：{row['分類']}")
        st.markdown(f"⭐ 評分：4.3 （模擬數值）")
        st.markdown("📌 **重點簡介：**")
        for point in row["條列簡介"]:
            st.markdown(f"- {point}")
    with cols[1]:
        st.link_button("查看完整內容 ➡️", f"/BookDetails?book={row['書名']}")
