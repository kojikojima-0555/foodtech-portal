import streamlit as st
import urllib.parse
from datetime import datetime

# 1. ページ設定と画面の余白調整
st.set_page_config(page_title="食品技術リサーチ・ランチャー", page_icon="🧪", layout="wide")

st.markdown("""
    <style>
    /* 画面上部の余白調整 */
    .block-container {
        padding-top: 2.5rem !important;
        padding-bottom: 1rem !important;
    }
    /* コマンドボックスの下部余白を詰める */
    div.stCode {
        margin-bottom: 0.5rem !important;
    }
    </style>
""", unsafe_allow_html=True)

# タイトルの装飾
st.markdown("<h2 style='font-size: 26px; line-height: 1.4; margin-top: 0px; margin-bottom: 15px; padding-top: 5px; padding-bottom: 0px;'>🧪 食品技術リサーチ・ランチャー</h2>", unsafe_allow_html=True)

# 現在の年（西暦）を自動取得
current_year = datetime.now().year

# 追加キーワードを記憶するための初期設定
if "custom_list" not in st.session_state:
    st.session_state.custom_list = []

# 2. サイドバー（条件設定画面）
with st.sidebar:
    st.header("条件設定")
    
    st.markdown("**1. テーマの選択・追加**")
    base_options = ["風味向上", "日持ち延長", "食感改良"]
    options = base_options + st.session_state.custom_list
    
    theme = st.multiselect("テーマ（複数選択可）", options, default=["日持ち延長"] + st.session_state.custom_list)
    custom_input = st.text_input("追加したいキーワード（あれば入力）", placeholder="例: 減塩、糖質オフ")
    
    if custom_input:
        new_items = [x.strip() for x in custom_input.replace("、", ",").split(",") if x.strip()]
        added = False
        for item in new_items:
            if item not in st.session_state.custom_list:
                st.session_state.custom_list.append(item)
                added = True
        if added:
            st.rerun()
    
    st.write("---")
    
    st.markdown("**2. 期間の指定**")
    period = st.slider("期間（発行年・出願年）", 2000, current_year, (2020, current_year))
    
    st.write("---")
    st.markdown("**3. 対象企業の指定**")
    comp = st.text_input("競合名・出願人（複数ある場合はスペース区切り）", value="キユーピー 味の素")

# 3. 検索式の自動組み立てロジック
if theme:
    themes_query = " OR ".join([f'"{t}"' for t in theme])
else:
    themes_query = ""

if comp:
    comp_list = [c.strip() for c in comp.replace(" ", " ").replace(",", " ").replace("、", " ").split(" ") if c.strip()]
    comp_query = " OR ".join([f'"{c}"' for c in comp_list])
    jp_comp_query = " OR ".join(comp_list)
else:
    comp_list = []
    comp_query = ""
    jp_comp_query = ""

scholar_query = ""
if themes_query and comp_query:
    if len(comp_list) > 1:
        scholar_query = f"({themes_query}) AND ({comp_query})"
    else:
        scholar_query = f"({themes_query}) AND {comp_query}"
elif themes_query:
    scholar_query = themes_query
elif comp_query:
    scholar_query = comp_query

encoded_scholar_query = urllib.parse.quote(scholar_query)
scholar_url = f"https://scholar.google.co.jp/scholar?q={encoded_scholar_query}&as_ylo={period[0]}&as_yhi={period[1]}"

# 4. 画面への出力表示
st.write("---")
st.markdown("<h4 style='font-size: 16px; margin-top:0px; margin-bottom:5px;'>📋 生成された検索リンク・特許コマンド</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🎓 学術論文 (Google Scholar)")
    st.info("※クリックすると、指定したキーワードと『期間指定』が自動適用されてGoogle Scholarが開きます。")
    
    if theme or comp_list:
        st.write(f"**生成されたクエリ:** `{scholar_query}`")
        st.link_button("Google Scholar で検索を実行", scholar_url, type="primary")
    else:
        st.warning("左側のサイドバーで条件を指定してください。")

with col2:
    st.markdown("##### 📑 特許検索 ([JP-NET](https://www.jp-net.jp/) 個別窓用)")
    st.info("※JP-NETの項目別入力画面の各窓に、コピーボタンを使って貼り付けてください。")
    
    if theme or comp_list:
        if theme:
            st.write("**🔍 キーワード欄 用:**")
            kw_cols = st.columns(2)
            for i, t in enumerate(theme):
                with kw_cols[i % 2]:
                    st.caption(f"キーワード {i+1}")
                    st.code(t, language="text")
            
        if comp_list:
            st.write("**🏢 出願人・権利者・企業名欄 用:**")
            st.code(jp_comp_query, language="text")
            
        st.write("---")
        # JP-NET（既存の青いボタン）
        st.link_button("JP-NET ログイン画面を開く", "https://www.jp-net.jp/", type="primary", use_container_width=True)
        
        # 💡 修正箇所: J-PlatPatボタンを読みやすいパステルグリーン×濃い緑文字に変更
        st.markdown("""
            <a href="https://www.j-platpat.inpit.go.jp/" target="_blank" style="
                display: block;
                width: 100%;
                text-align: center;
                background-color: #E8F5E9; /* 目に優しいパステルグリーン */
                color: #1B5E20 !important; /* 文字を濃い緑にして視認性を確保 */
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;          /* 太字にして読みやすさをアップ */
                text-decoration: none;
                border-radius: 8px;
                box-sizing: border-box;
                margin-top: 8px;
                border: 1px solid #C8E6C9; /* 輪郭をはっきりさせるための薄い枠線 */
            ">簡易検索はこちら：特許情報プラットフォーム (J-PlatPat)</a>
        """, unsafe_allow_html=True)
    else:
        st.warning("左側のサイドバーで条件を指定してください。")

# 5. セキュリティに関する安心ガイド
st.write("---")
st.markdown("""
<details>
<summary>🔒 <b>本システムのセキュリティと安全性の担保について（IT管理者向け）</b></summary>
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; color: #31333F; font-size: 13px;">
<ul>
    <li><b>外部通信の排除</b>: 本アプリは、入力された文字列をブラウザ上でURLやコピー用テキストに変換するだけの「静的なナビゲーター」です。外部のAIやデータベースへデータを送信することは一切ありません。</li>
    <li><b>アカウント情報の保護</b>: JP-NET等のIDやパスワードをプログラムに入力・保存する領域自体が存在しないため、なりすましや不正アクセスのリスクは構造上0%です。</li>
    <li><b>スクレイピングの不保持</b>: 自動でデータを引っこ抜くようなスクレイピング処理は含まれておらず、あくまでユーザー自身のブラウザの挙動を補助する仕組み（便利リンク）であるため、各サービスの利用規約を完全に遵守しています。</li>
</ul>
</div>
</details>
""", unsafe_allow_html=True)
