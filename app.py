import streamlit as st
import google.generativeai as genai
from datetime import datetime

# --- 1. API設定 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("APIキー設定エラー")
    st.stop()

# --- 2. 高速化のためのキャッシュ関数 ---
# 同じ検索条件なら、AIを動かさずキャッシュから即座に返します
@st.cache_data(ttl=3600) # 1時間は同じ結果を保持
def get_ai_response(themes, period, competitor):
    model = genai.GenerativeModel('gemini-3-flash')
    
    # 処理を早くするため、AIに「簡潔さ」を命じるプロンプトに変更
    prompt = f"""
    食品技術コンサルタントとして、{period[0]}-{period[1]}年の{themes}に関する最新技術を報告せよ。
    競合動向: {competitor if competitor else '主要各社'}
    
    【ルール】挨拶不要。即、箇条書きで結論を書くこと。
    1. トレンド(3点)
    2. 注目技術(3点): 技術名、原理、日持ち/風味/食感への効果
    3. 推奨アクション(2点)
    """
    
    # ストリーミングではなく、一括で取得してキャッシュに保存
    response = model.generate_content(prompt)
    return response.text

# --- 3. UI設定 ---
st.set_page_config(page_title="高速・食品技術ポータル", layout="wide")

st.title("🧪 高速・食品技術インテリジェンス")

# サイドバー
with st.sidebar:
    st.header("条件設定")
    themes = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    competitor = st.text_input("競合名")
    if st.button("キャッシュをクリア"):
        st.cache_data.clear()

# --- 4. 実行部分 ---
if st.button("インテリジェンス生成"):
    start_time = datetime.now()
    
    with st.spinner("AIが解析中..."):
        # キャッシュされた関数を呼び出し
        result = get_ai_response(themes, period, competitor)
        
        st.markdown(result)
        
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds()
    st.caption(f"解析完了時間: {duration:.1f}秒 (キャッシュが効くと0秒になります)")

else:
    st.write("左で条件を選び、ボタンを押してください。2回目以降の同じ検索は一瞬で終わります。")
