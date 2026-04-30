import streamlit as st
import google.generativeai as genai

# --- 1. API設定 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("APIキーをSecretsに設定してください")
    st.stop()

# --- 2. 画面デザイン（軽量化） ---
st.set_page_config(page_title="爆速！食品技術ポータル", page_icon="⚡")
st.markdown("""
    <style>
    .stProgress > div > div > div > div { background-color: #1e3a8a; }
    section[data-testid="stSidebar"] { width: 250px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. メインロジック ---
st.title("⚡ 食品技術インテリジェンス・ターボ")

with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", placeholder="例: キユーピー")
    st.divider()
    if st.button("キャッシュクリア"):
        st.cache_data.clear()

# 検索ボタン
if st.button("インテリジェンス生成"):
    # プロンプトを極限まで効率化（AIの思考時間を削る）
    themes_txt = "、".join(theme)
    prompt = f"""
    食品技術コンサルとして{period[0]}-{period[1]}年の{themes_txt}（競合:{comp}）の最新技術を報告せよ。
    【制約】
    - 前置き・挨拶一切不要。
    - 重要な3点のみ、各100文字以内で結論から書け。
    - 形式: 項目名、技術核心、R&D示唆。
    - 専門用語を使いつつ、簡潔に。
    """

    # ストリーミング表示（AIが考えたそばから表示）
    st.subheader("📊 解析結果（リアルタイム生成）")
    
    # プレースホルダー（空の枠）を作って、そこに文字を流し込む
    report_placeholder = st.empty()
    
    model = genai.GenerativeModel('gemini-1.5-flash')
    
    # AIの回答を少しずつ表示
    try:
        # st.write_streamを使うことで「待たされている感」をゼロにします
        full_response = st.write_stream(model.generate_content(prompt, stream=True))
        
        # 完了後に結果をキャッシュ的なログとして保存（オプション）
        st.success(f"解析完了")
        
    except Exception as e:
        st.error(f"エラーが発生しました: {e}")

else:
    st.info("左の条件を選び、上のボタンを押してください。")
