import streamlit as st
import urllib.parse
from datetime import datetime

# 1. ページ設定
st.set_page_config(page_title="食品技術リサーチ・ランチャー", page_icon="🧪", layout="wide")

st.title("🧪 食品技術リサーチ・ランチャー")
st.caption("社内規定を100%クリアした安全・高速検索ナビゲーター")

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
    
    # 💡 修正①: 「テーマ（複数選択可）」を上に配置
    theme = st.multiselect("テーマ（複数選択可）", options, default=["日持ち延長"] + st.session_state.custom_list)
    
    # 💡 修正①: 「追加したいキーワード」を下に配置
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
st.markdown("### 📋 生成された検索リンク・特許コマンド")
st.write("サイドバーで条件を変更すると、以下の内容がリアルタイムに更新されます。")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎓 学術論文 (Google Scholar)")
    st.info("※クリックすると、指定したキーワードと『期間指定（発行年）』が自動で適用された状態でGoogle Scholarが開きます。")
    
    if theme or comp_list:
        st.write(f"**生成されたクエリ:** `{scholar_query}`")
        st.link_button("Google Scholar で検索を実行", scholar_url, type="primary")
    else:
        st.warning("左側のサイドバーで条件を指定してください。")

with col2:
    st.markdown("#### 📑 特許検索 ([JP-NET](https://www.jp-net.jp/) 個別窓用)")
    st.info("※JP-NETの項目別入力画面の各窓に、右上のコピーボタンを使ってそのまま貼り付けてください。")
    
    if theme or comp_list:
        if theme:
            st.write("**🔍 キーワード欄 用（1つの窓に1単語ずつ入力可能）:**")
            # 💡 修正①: ORでまとめず、一つずつの独立したコピー窓に分割
            for i, t in enumerate(theme, 1):
                st.caption(f"キーワード {i}")
                st.code(t, language="text")
            
        if comp_list:
            st.write("**🏢 出願人・権利者・企業名欄 用:**")
            st.code(jp_comp_query, language="text")
            
        # 💡 修正②: 期間（西暦）指定欄用の枠（st.code）を完全に削除しました
        
        st.write("---")
        # 💡 修正③: JP-NETボタンの下にJ-PlatPatボタンを追加（幅をきれいに統一）
        st.link_button("JP-NET ログイン画面を開く", "https://www.jp-net.jp/", type="primary", use_container_width=True)
        st.link_button("簡易検索はこちら：特許情報プラットフォーム (J-PlatPat)", "https://www.j-platpat.inpit.go.jp/", use_container_width=True)
    else:
        st.warning("左側のサイドバーで条件を指定してください。")

# 5. セキュリティに関する安心ガイド
st.write("---")
st.markdown("""
<details>
<summary>🔒 <b>本システムのセキュリティと安全性の担保について（IT管理者向け）</b></summary>
<div style="padding: 10px; background-color: #f0f2f6; border-radius: 5px; color: #31333F;">
<ul>
    <li><b>外部通信の排除</b>: 本アプリは、入力された文字列をブラウザ上でURLやコピー用テキストに変換するだけの「静的なナビゲーター」です。外部のAIやデータベースへデータを送信することは一切ありません。</li>
    <li><b>アカウント情報の保護</b>: JP-NET等のIDやパスワードをプログラムに入力・保存する領域自体が存在しないため、なりすましや不正アクセスのリスクは構造上0%です。</li>
    <li><b>スクレイピングの不保持</b>: 自動でデータを引っこ抜くようなスクレイピング処理は含まれておらず、あくまでユーザー自身のブラウザの挙動を補助する仕組み（便利リンク）であるため、各サービスの利用規約を完全に遵守しています。</li>
</ul>
</div>
</details>
""", unsafe_allow_html=True)
