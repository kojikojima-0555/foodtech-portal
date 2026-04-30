import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="食品技術ポータル・実況版", page_icon="🧪")

# API初期化関数
def init_api():
    st.write("🔍 ステップ1: SecretsからAPIキーを読み込み中...")
    if "GEMINI_API_KEY" not in st.secrets:
        st.error("❌ Secretsに 'GEMINI_API_KEY' がありません")
        return None
    
    api_key = st.secrets["GEMINI_API_KEY"]
    st.write("🔍 ステップ2: Google AIに接続中...")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel('gemini-1.5-flash')

st.title("🧪 食品技術インテリジェンス（実況中継版）")

with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名", value="キユーピー")

if st.button("インテリジェンス生成"):
    # ステップごとに画面に文字を出します
    model = init_api()
    
    if model:
        st.write("🔍 ステップ3: プロンプトを作成完了")
        prompt = f"食品技術の調査報告。テーマ：{theme}。期間：{period[0]}-{period[1]}年。競合：{comp}。具体的な技術例を2点教えて。"

        st.write("🔍 ステップ4: AIに送信しました。返信を待っています（ここが最長30秒かかります）...")
        
        try:
            # タイムアウトを避けるため、最もシンプルな呼び出し
            response = model.generate_content(prompt)
            
            st.write("🔍 ステップ5: AIからデータが届きました。表示します。")
            
            if response:
                st.subheader("📊 解析結果")
                st.markdown(response.text)
                st.success("✅ 全行程が正常に終了しました")
            else:
                st.warning("⚠️ 応答が空です")
                
        except Exception as e:
            st.error(f"❌ 通信中にトラブル発生: {e}")
            st.info("これが表示される場合、APIキーの制限かGoogle側のサーバー混雑の可能性があります。")

else:
    st.info("サイドバーで条件を設定し、上のボタンをクリックしてください。")
