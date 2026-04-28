import streamlit as st
import google.generativeai as genai
from datetime import datetime
import time

# --- 1. 設定: Gemini API Key (Secretsから取得) ---
# Streamlit CloudのSettings > Secretsで GEMINI_API_KEY を設定している前提です
try:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception:
    st.error("APIキーが設定されていません。StreamlitのSecrets設定を確認してください。")
    st.stop()

# --- 2. ページ基本設定 ---
st.set_page_config(
    page_title="次世代食品技術インテリジェンス・ポータル",
    page_icon="🧪",
    layout="wide"
)

# デザインの調整（フォントサイズや背景色）
st.markdown("""
    <style>
    .report-card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #ffffff;
        border-left: 6px solid #1e3a8a;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #1e3a8a;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. サイドバー: 分析条件の入力 ---
with st.sidebar:
    st.title("🎛️ 分析コントロール")
    st.write("検索条件をカスタマイズしてください")
    
    target_themes = st.multiselect(
        "ターゲットテーマ",
        ["風味向上", "日持ち延長", "食感改良"],
        default=["風味向上", "日持ち延長", "食感改良"]
    )
    
    period = st.slider("対象期間 (年)", 2023, 2026, (2023, 2026))
    
    competitor = st.text_input(
        "注目競合・企業名", 
        placeholder="例: キユーピー, 味の素, Every Company"
    )
    
    st.divider()
    st.caption(f"© 2026 食品技術コンサルタント AI Port v2.0")

# --- 4. メイン画面の構成 ---
st.title("🧪 次世代食品技術インテリジェンス・ポータル")
st.subheader("卵・調味料領域の国内外特許・論文自動解析システム")
st.write(f"---")

# 実行ボタン
if st.button("最新インテリジェンスを生成（ストリーミング開始）"):
    
    # プロンプトの作成
    themes_str = "、".join(target_themes)
    prompt = f"""
    あなたは超優秀な食品技術コンサルタントです。
    {period[0]}年から{period[1]}年までの、{themes_str}に関する国内外の最新特許、論文、
    および競合他社（{competitor if competitor else '主要企業'}）の動向を調査し、
    以下の3つの構成でプロフェッショナルな日本語レポートを作成してください。

    1. 【要点要約】: 業界全体の大きな流れ（トレンド）を3点。
    2. 【注目技術カード】: 重要な技術（特許・論文）を3〜4つ。各カードには「技術の核心」「ターゲットへの寄与」「実務への示唆」を含めること。
    3. 【戦略的提言】: 収集した情報に基づき、自社が今すぐ着手すべきR&Dアクションを2点。

    出力はマークダウン形式で行い、読みやすく装飾してください。
    専門用語（乳化、静菌、離水、呈味成分など）は正確に使用してください。
    """

    # 解析ステータスの表示
    status = st.status("🚀 情報収集および解析中...", expanded=True)
    status.write("グローバルデータベースへアクセス中...")
    time.sleep(1)
    status.write(f"{themes_str}に関連する文献をフィルタリング中...")
    time.sleep(1)
    status.write("Gemini 3 Flashによる技術的解釈を開始...")

    # ストリーミング表示エリアの確保
    report_area = st.container()
    
    with report_area:
        st.markdown("### 📊 最新インテリジェンス・レポート")
        # ここがストリーミングの核心部分
        model = genai.GenerativeModel('gemini-3-flash')
        response = model.generate_content(prompt, stream=True)
        
        # 文章を少しずつ表示していく
        st.write_stream(response)

    status.update(label="✅ 解析完了", state="complete", expanded=False)
    
    # 完了後のアクション
    st.success("最新の技術情報を取得しました。")
    st.download_button(
        label="レポートをテキストとして保存",
        data=st.session_state.get('last_response', ""), # 簡易的な保存例
        file_name=f"FoodTech_Report_{datetime.now().strftime('%Y%m%d')}.txt",
        mime="text/plain"
    )

else:
    # 初期表示画面
    col1, col2 = st.columns([2, 1])
    with col1:
        st.info("👈 左側のサイドバーから条件を設定し、ボタンを押してください。")
        st.write("""
        #### このポータルで解決できること：
        * **情報の飽和:** 毎日溢れる論文や特許から、本当に価値のあるものだけを抽出します。
        * **言語の壁:** 海外の最新技術を、専門用語を維持したまま日本語で理解できます。
        * **意思決定の遅れ:** 調査・分析にかかる時間を数日から数秒へ短縮します。
        """)
    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/2103/2103633.png", width=150)
