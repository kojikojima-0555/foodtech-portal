import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="食品技術ポータル・最終安定版", page_icon="🧪")

# 2. API初期化（エラー時は画面に表示）
def init_api():
    try:
        api_key = st.secrets["GEMINI_API_KEY"]
        genai.configure(api_key=api_key)
        # 安全設定：技術情報なのでフィルターを最小限にする
        safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        return genai.GenerativeModel('gemini-1.5-flash', safety_settings=safety_settings)
    except Exception as e:
        st.error(f"API初期化エラー: {e}")
        return None

# UI表示
st.title("🧪 食品技術インテリジェンス")

with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", placeholder="例: キユーピー")

# 実行ボタン
if st.button("インテリジェンス生成"):
    model = init_api()
    if model:
        themes_txt = "、".join(theme)
        prompt = f"""
        あなたは優秀な食品技術コンサルタントです。
        {period[0]}年から{period[1]}年までの、{themes_txt}（競合：{comp}）に関する
        最新の技術トレンド、特許、論文の要点を3つ、日本語で解説してください。
        回答は必ず日本語で、箇条書きを使って分かりやすく記述してください。
        """

        with st.spinner("AIが技術文書を解析中...（約10〜20秒かかります）"):
            try:
                # ストリーミングをオフにし、一括で取得する方式に変更
                response = model.generate_content(prompt)
                
                # 結果が表示可能かチェック
                if response and response.text:
                    st.subheader("📊 解析結果")
                    st.markdown(response.text)
                    st.success("解析が完了しました。")
                else:
                    st.warning("AIから有効な回答が得られませんでした。条件を変えて再度お試しください。")
                    
            except Exception as e:
                st.error(f"解析中にエラーが発生しました。詳細: {e}")
    else:
        st.error("APIの準備ができていません。")

else:
    st.info("サイドバーで条件を設定し、ボタンをクリックしてください。")
