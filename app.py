import streamlit as st
import google.generativeai as genai

st.title("API接続テスト")

# 1. APIキー読み込み
api_key = st.secrets["GEMINI_API_KEY"]
genai.configure(api_key=api_key)

# 2. ボタンを押したら「こんにちは」とだけ送る
if st.button("テスト実行"):
    st.write("🔍 AIに接続しています...")
    
    try:
        # 最も軽いモデルと、最も短いプロンプト
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        # 1語だけ返してもらう（タイムアウト回避）
        response = model.generate_content("こんにちは、とだけ日本語で返してください。")
        
        if response.text:
            st.success("✅ 通信成功！")
            st.write("AIからの返信:", response.text)
        else:
            st.warning("⚠️ 返信が空でした。")
            
    except Exception as e:
        st.error(f"❌ 通信エラー発生: {e}")
