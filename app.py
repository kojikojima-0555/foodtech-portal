import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="食品技術ポータル・最終解決版", page_icon="🧪")

def init_api():
    st.write("🔍 ステップ1: キー読み込み...")
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    
    # 【重要】安全フィルターをすべて無効化して、ブロックによるフリーズを防ぎます
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]
    
    return genai.GenerativeModel(
        model_name='gemini-1.5-flash',
        safety_settings=safety_settings
    )

st.title("🧪 食品技術インテリジェンス（解決版）")

with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", value="キユーピー")

if st.button("インテリジェンス生成"):
    model = init_api()
    
    if model:
        st.write("🔍 ステップ2: AIへのリクエストを準備中...")
        # 非常に短く、AIが拒否しにくいプロンプトに変更
        prompt = f"食品の{theme}に関する最新技術（2023-2026）を1つ、日本語で短く説明してください。"

        st.write("🔍 ステップ3: 送信。AIの返信を待っています...")
        
        try:
            # ストリーミングを使わず、かつ短い時間で結果が出るようにします
            response = model.generate_content(prompt)
            
            # ブロックされたかどうかを確認
            if response.candidates:
                candidate = response.candidates[0]
                # もし安全上の理由で止まっていたらその理由を出す
                if candidate.finish_reason != 1: # 1は正常終了
                    st.warning(f"⚠️ AIが回答を制限しました。理由コード: {candidate.finish_reason}")
                
                if hasattr(candidate.content, "parts") and candidate.content.parts:
                    st.subheader("📊 解析結果")
                    st.markdown(response.text)
                    st.success("✅ 成功しました！")
                else:
                    st.error("❌ 回答のパーツが空です。")
            else:
                st.error("❌ 回答候補が見つかりませんでした。")
                
        except Exception as e:
            st.error(f"❌ 通信エラー: {e}")
            st.info("APIキーが『Google AI Studio』で作成された『無料枠』の場合、1分あたりの回数制限に達している可能性があります。少し待ってから再度お試しください。")

else:
    st.info("ボタンを押すと開始します。")
