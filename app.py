import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 設定: Gemini API Key ---
API_KEY = "YOUR_GEMINI_API_KEY" 
genai.configure(api_key=API_KEY)

# --- UI設定 ---
st.set_page_config(page_title="FoodTech Intelligence Portal", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stHeading { color: #1e3a8a; }
    </style>
    """, unsafe_allow_html=True)

# --- サイドバー ---
with st.sidebar:
    st.title("分析コントロール")
    target_theme = st.multiselect(
        "ターゲットテーマ",
        ["風味向上", "日持ち延長", "食感改良"],
        default=["日持ち延長"]
    )
    period = st.slider("対象期間", 2023, 2026, (2023, 2026))
    competitor = st.text_input("注目競合 (任意)", placeholder="例: キユーピー")

# --- メイン画面 ---
st.title("🧪 次世代食品技術インテリジェンス・ポータル")
st.caption(f"最終更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if st.button("最新インテリジェンスを生成"):
    with st.spinner("グローバルデータベースから情報を収集中..."):
        prompt = f"{period[0]}年から{period[1]}年までの、{target_theme}に関する最新の特許、論文、競合（{competitor}）の動向を4つのカード形式で要約して。"
        model = genai.GenerativeModel('gemini-3-flash')
        response = model.generate_content(prompt)
        st.markdown(response.text)
else:
    st.write("### 👈 サイドバーから条件を設定して、最新のインテリジェンスを取得してください。")
