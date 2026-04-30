import streamlit as st
import google.generativeai as genai

# 1. ページ設定
st.set_page_config(page_title="食品技術ポータル・診断版", page_icon="🧪")

# 2. API初期化
def init_api():
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("Secretsに 'GEMINI_API_KEY' が設定されていません。")
        return None
    
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # モデル設定（安全設定を極限まで緩め、エラーを防ぎます）
    model = genai.GenerativeModel('gemini-1.5-flash')
    return model

# UI表示
st.title("🧪 食品技術インテリジェンス")

with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", placeholder="例: キユーピー")

# ボタン押下時
if st.button("インテリジェンス生成"):
    model = init_api()
    
    if model:
        themes_txt = "、".join(theme)
        # プロンプトを極めてシンプルにし、AIの「拒否」を防ぎます
        prompt = f"食品技術の調査報告。テーマ：{themes_txt}。期間：{period[0]}年から{period[1]}年。競合：{comp}。これらについて、具体的な技術例を3点日本語で教えてください。"

        with st.spinner("AIと通信中..."):
            try:
                # タイムアウトやブロックを確認するため、あえてシンプルな呼び出し
                response = model.generate_content(prompt)
                
                # --- デバッグ機能：応答の中身をチェック ---
                if not response.candidates:
                    st.error("AIからの回答が空でした。APIキーの制限か、プロンプトがブロックされた可能性があります。")
                else:
                    try:
                        # 正常にテキストが出力される場合
                        st.subheader("📊 解析結果")
                        st.markdown(response.text)
                        st.success("解析成功")
                    except ValueError:
                        # 安全フィルターでブロックされた場合、原因を表示
                        st.warning("AIの回答が安全フィルターによってブロックされました。")
                        st.write("理由の確認:", response.prompt_feedback)
            
            except Exception as e:
                # エラーが起きたらその内容をそのまま表示
                st.error(f"致命的なエラーが発生しました: {e}")
                st.info("ヒント: APIキーが正しいか、Google AI Studioで有効になっているか確認してください。")
    else:
        st.error("APIの準備ができていません。")

else:
    st.info("サイドバーで条件を設定し、ボタンをクリックしてください。")
