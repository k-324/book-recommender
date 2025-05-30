import streamlit as st

# ✅ 開發模式：快速測試畫面不載模型
DEV_MODE = True

# ✅ 主標題
st.title("📘 Book一試")

# ✅ 子標題說明
st.markdown("請輸入你的閱讀需求，讓我們推薦符合你心情或興趣的書籍！")

# ✅ 使用者輸入欄
user_input = st.text_area("📝 你有什麼樣的需求呢？", placeholder="例如：我最近壓力很大，想找些療癒系的書...")

# ✅ 按鈕
if st.button("推薦給我"):
    if user_input.strip():
        st.success("（這裡會顯示針對你輸入的推薦結果）")
    else:
        st.warning("請先輸入你的需求喔！")

# ✅ 開發模式提示
if DEV_MODE:
    st.warning("⚠️ 開發模式開啟中：未載入模型與嵌入")
