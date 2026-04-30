import streamlit as st
import google.generativeai as genai

# --- 1. API設定 ---
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("APIキーをSecretsに設定してください")
    st.stop()

# --- 2. 画面設定 ---
st.set_page_config(page_title="確実動作版・食品ポータル", page_icon="🧪")

st.title("🧪 食品技術インテリジェンス")

# サイドバー設定
with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", placeholder="例: キユーピー")
    if st.button("キャッシュクリア"):
        st.cache_data.clear()

# --- 3. 実行メイン処理 ---
if st.button("インテリジェンス生成"):
    themes_txt = "、".join(theme)
    prompt = f"{period[0]}-{period[1]}年の{themes_txt}（競合:{comp}）の最新技術を3点、箇条書きで簡潔に報告せよ。"

    st.subheader("📊 解析結果")
    
    # 文字を流し込むための空の枠を作成
    placeholder = st.empty()
    full_text = ""
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        # ストリーミング生成を開始
        response = model.generate_content(prompt, stream=True)
        
        for chunk in response:
            if chunk.text:
                full_text += chunk.text
                # 枠の中に、今届いた文字をリアルタイムで表示（カーソル風の ▌ を追加）
                placeholder.markdown(full_text + " ▌")
        
        # 最後にカーソルを取って、きれいに表示
        placeholder.markdown(full_text)
        st.success("解析が完了しました。")

    except Exception as e:
        st.error(f"エラーが発生しました。時間を置いて再度お試しください。内容: {e}")

else:
    st.info("条件を選んでボタンを押してください。")
