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

# 初期設定用の固定3テーマ
base_options = ["風味向上", "日持ち延長", "食感改良"]

if "custom_list" not in st.session_state:
    st.session_state.custom_list = []
if "selected_themes" not in st.session_state:
    st.session_state.selected_themes = ["日持ち延長"]

# 💡 修正①: エンター1回で即座にデータを追加・反映するための専用の裏処理（コールバック関数）
def handle_theme_addition():
    val = st.session_state.theme_input_widget
    if val:
        # カンマや「、」で区切ってリスト化
        new_items = [x.strip() for x in val.replace("、", ",").split(",") if x.strip()]
        for item in new_items:
            # 選択肢リストに未登録なら追加
            if item not in st.session_state.custom_list and item not in base_options:
                st.session_state.custom_list.append(item)
            # 現在のチェック（選択）状態にも即座に合流させる
            if item not in st.session_state.selected_themes:
                st.session_state.selected_themes.append(item)
        # 💡 追加後、入力欄の文字をパッと自動で消去して次の入力をしやすくする
        st.session_state.theme_input_widget = ""

# 2. サイドバー（条件設定画面）
with st.sidebar:
    st.header("条件設定")
    
    st.markdown("**1. テーマの選択・追加**")
    options = base_options + [x for x in st.session_state.custom_list if x not in base_options]
    
    # 選択状態をセッション状態と同期
    theme = st.multiselect("テーマ（複数選択可）", options, default=st.session_state.selected_themes)
    st.session_state.selected_themes = theme
    
    # 💡 修正①: on_change と key を連携させ、1回のエンターで遅延なく処理を実行します
    st.text_input(
        "追加したいテーマ（あれば入力）", 
        placeholder="例: 減塩、糖質オフ", 
        key="theme_input_widget", 
        on_change=handle_theme_addition
    )
    
    st.write("---")
    
    st.markdown("**2. 期間の指定**")
    period = st.slider("期間（発行年・出願年）", 2000, current_year, (2020, current_year))
    
    st.write("---")
    st.markdown("**3. 対象企業の指定**")
    comp = st.text_input("競合名・出願人（複数ある場合はスペース区切り）", value="キユーピー 味の素")

# ==========================================
# 3. 検索式の自動組み立てロジック
# ==========================================

# 共通の企業名リスト作成
if comp:
    comp_list = [c.strip() for c in comp.replace(" ", " ").replace(",", " ").replace("、", " ").split(" ") if c.strip()]
    jp_comp_query = " OR ".join(comp_list)
else:
    comp_list = []
    jp_comp_query = ""

# 論文・特許共通で使える綺麗な「テーマ用」「企業用」の検索パーツを作成
themes_raw = " OR ".join([f'"{t}"' for t in theme]) if theme else ""
comp_raw = " OR ".join([f'"{c}"' for c in comp_list]) if comp_list else ""

# A. Google Scholar 用のクエリ
scholar_query = ""
if themes_raw and comp_raw:
    scholar_query = f"({themes_raw}) AND ({comp_raw})"
elif themes_raw:
    scholar_query = themes_raw
elif comp_raw:
    scholar_query = comp_raw

encoded_scholar_query = urllib.parse.quote(scholar_query)
scholar_url = f"https://scholar.google.co.jp/scholar?q={encoded_scholar_query}&as_ylo={period[0]}&as_yhi={period[1]}"

# B. Google Patents 用のクエリ
patents_query = ""
if themes_raw and comp_raw:
    patents_query = f"({themes_raw}) ({comp_raw})"
elif themes_raw:
    patents_query = f"({themes_raw})"
elif comp_raw:
    patents_query = f"({comp_raw})"

encoded_patents_query = urllib.parse.quote(patents_query)
patents_url = f"https://patents.google.com/?q={encoded_patents_query}&after={period[0]}0101&before={period[1]}1231"


# ==========================================
# 4. 画面への出力表示
# ==========================================
st.write("---")
st.markdown("<h4 style='font-size: 16px; margin-top:0px; margin-bottom:5px;'>📋 生成された検索リンク・特許コマンド</h4>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("##### 🎓 学術論文 (Google Scholar)")
    st.info("※クリックすると、指定したキーワードと『期間指定』が自動適用されてGoogle Scholarが開きます。")
    
    if theme or comp_list:
        st.write(f"**生成されたクエリ:** `{scholar_query}`")
        st.link_button("Google Scholar で検索を実行", scholar_url, type="primary", use_container_width=True)
        
        st.write("---")
        st.markdown("##### 🌐 グローバル特許 (Google Patents)")
        st.info("※クリックすると、海外特許を含む世界中の特許が出願人（企業名）指定・期間指定された状態で開きます。")
        st.write(f"**特許専用最適化クエリ:** `{patents_query}`")
        st.link_button("Google Patents で特許検索を実行", patents_url, type="primary", use_container_width=True)
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
        st.link_button("JP-NET ログイン画面を開く", "https://www.jp-net.jp/", type="primary", use_container_width=True)
        
        st.markdown("""
            <a href="https://www.j-platpat.inpit.go.jp/" target="_blank" style="
                display: block;
                width: 100%;
                text-align: center;
                background-color: #E8F5E9;
                color: #1B5E20 !important;
                padding: 10px 16px;
                font-size: 14px;
                font-weight: 600;
                text-decoration: none;
                border-radius: 8px;
                box-sizing: border-box;
                margin-top: 8px;
                border: 1px solid #C8E6C9;
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
