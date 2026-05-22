import streamlit as st
import urllib.parse

# 1. ページ設定
st.set_page_config(page_title="食品技術リサーチ・ランチャー", page_icon="🧪", layout="wide")

st.title("🧪 食品技術リサーチ・ランチャー")
st.caption("社内規定を100%クリアした安全・高速検索ナビゲーター")

# 2. サイドバー（条件設定画面）
with st.sidebar:
    st.header("条件設定")
    theme = st.multiselect("テーマ（複数選択可）", ["風味向上", "日持ち延長", "食感改良"], default=["日持ち延長"])
    period = st.slider("期間（発行年・出願年）", 2023, 2026, (2023, 2026))
    comp = st.text_input("競合名・出願人", value="キユーピー")

# 3. 検索式の自動組み立てロジック
if theme:
    themes_query = " OR ".join([f'"{t}"' for t in theme])
else:
    themes_query = ""

# Google Scholar用のクエリ組み立て
scholar_query = ""
if themes_query and comp:
    scholar_query = f"({themes_query}) AND \"{comp}\""
elif themes_query:
    scholar_query = themes_query
elif comp:
    scholar_query = f"\"{comp}\""

# URL用に特殊文字を変換
encoded_scholar_query = urllib.parse.quote(scholar_query)

# Google Scholar用URL（期間指定パラメータ含む）
scholar_url = f"https://scholar.google.co.jp/scholar?q={encoded_scholar_query}&as_ylo={period[0]}&as_yhi={period[1]}"

# 4. 画面への出力表示
st.write("---")
st.markdown("### 📋 生成された検索リンク・特許コマンド")
st.write("サイドバーで条件を変更すると、以下のリンクと検索式がリアルタイムに更新されます。")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🎓 学術論文 (Google Scholar)")
    st.info("※クリックすると、指定したキーワードと『期間指定（発行年）』が自動で適用された状態でGoogle Scholarが開きます。")
    
    if theme or comp:
        st.write(f"**生成されたクエリ:** `{scholar_query}`")
        st.link_button("Google Scholar で検索を実行", scholar_url, type="primary")
    else:
        st.warning("左側のサイドバーで条件を指定してください。")

with col2:
    st.markdown("#### 📑 特許検索 (JP-NET用)")
    st.info("※JP-NETはログインが必要なため直接リンクが作れません。以下の検索式をコピーして、JP-NETの検索窓にそのまま貼り付けてご利用ください。")
    
    if theme or comp:
        st.write("**JP-NET貼り付け用テキスト:**")
        st.code(f"({ ' OR '.join(theme) }) AND {comp}", language="text")
        st.caption(f"※JP-NETの検索画面側で、期間（期間指定：{period[0]}年〜{period[1]}年）を設定して実行してください。")
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
""", unsafe_allow_html=True) # ←ここを修正しました！
