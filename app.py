import streamlit as st
import google.generativeai as genai

st.title("最終接続診断")

# 1. Secretsの読み込みチェック
st.write("### 🔍 診断ステップ1: 設定の確認")
if "GEMINI_API_KEY" not in st.secrets:
    st.error("❌ Secretsの中に 'GEMINI_API_KEY' という項目が見つかりません。")
    st.stop()

key = st.secrets["GEMINI_API_KEY"]
st.write(f"・キーの存在: ✅ 確認 (長さ: {len(key)}文字)")

if key.startswith("AIza") is False:
    st.error("❌ エラー: キーが 'AIza' で始まっていないようです。コピーミスがないか確認してください。")
    st.stop()

# 2. 設定の適用
st.write("### 🔍 診断ステップ2: 接続テスト")
if st.button("今すぐ接続テストを実行"):
    try:
        genai.configure(api_key=key)
        # タイムアウトを極短（10秒）に設定して、無限に待つのを防ぐ
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("AIにメッセージを送信中... (10秒以内に反応がなければ通信ブロックです)")
        
        # 究極に短いリクエスト
        response = model.generate_content("Hi", request_options={"timeout": 10})
        
        if response:
            st.success("✅ 成功しました！")
            st.write("AIからの返答:", response.text)
            st.balloons()
            
    except Exception as e:
        st.error(f"❌ 接続エラーが発生しました: {e}")
        st.write("このエラーメッセージを教えてください。")
