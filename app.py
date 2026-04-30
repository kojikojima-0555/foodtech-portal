import streamlit as st
import google.generativeai as genai

# 1. 画面の基本設定
st.set_page_config(page_title="食品技術ポータル・安定版", page_icon="🧪")

# 2. APIキーの読み込みとチェック
def init_api():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ エラー: Streamlitの『Secrets』に『GEMINI_API_KEY』が見つかりません。設定を確認してください。")
        st.stop()
    
    api_key = st.secrets["GEMINI_API_KEY"]
    if not api_key or api_key == "ここにAPIキーを貼り付ける":
        st.error("❌ エラー: APIキーが正しく設定されていません。")
        st.stop()
        
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

# アプリのメイン表示
st.title("🧪 食品技術インテリジェンス")

# サイドバー
with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", placeholder="例: キユーピー")

# 実行処理
if st.button("インテリジェンス生成"):
    model = init_api() # ここでAPIを初期化
    
    themes_txt = "、".join(theme)
    prompt = f"{period[0]}-{period[1]}年の{themes_txt}（競合:{comp}）に関する最新技術トレンドと具体的な技術例を3点、日本語で簡潔に報告してください。"

    st.subheader("📊 解析結果")
    placeholder = st.empty()
    full_text = ""
    
    try:
        # ストリーミング生成
        responses = model.generate_content(prompt, stream=True)
        
        for response in responses:
            if response.text:
                full_text += response.text
                placeholder.markdown(full_text + " ▌")
        
        placeholder.markdown(full_text)
        st.success("解析が完了しました。")

    except Exception as e:
        st.error(f"❌ 解析中にエラーが発生しました。以下の内容を確認してください:\n\n{str(e)}")

else:
    st.info("条件を選んでボタンを押してください。")
