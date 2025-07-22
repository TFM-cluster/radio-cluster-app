import streamlit as st
from PIL import Image
import pandas as pd

# ページ設定
st.set_page_config(page_title="Airlytics", page_icon="📻", layout="centered")

# ロゴ画像
logo = Image.open("Airlytics.png")
st.image(logo, use_column_width=True)

# タイトル
st.markdown(
    """
    <h1 style='text-align: center; color: #333;'>Airlytics</h1>
    <h3 style='text-align: center; color: #666;'>📊 ラジオAI：時間帯クラスタ診断</h3>
    """,
    unsafe_allow_html=True
)

# データ読み込み（CSV）
@st.cache_data
def load_data():
    return pd.read_csv("cluster_by_time.csv")

df = load_data()

# 入力UI
st.markdown("### 🔍 曜日と時間帯を選択してください")
weekday = st.selectbox("曜日を選んでください", df["曜日"].unique())
hour = st.slider("時間を選んでください（24h形式、5〜29）", min_value=5, max_value=29, value=9)

# 診断
match = df[(df["曜日"] == weekday) & (df["開始時"] == hour)]
if not match.empty:
    cluster = match.iloc[0]["推定クラスタ"]
    st.success(f"✅ {weekday}曜 {hour}時台 は『クラスター {cluster}』です")

    # 同じクラスタの他時間帯
    others = df[(df["推定クラスタ"] == cluster) & ~((df["曜日"] == weekday) & (df["開始時"] == hour))]
    if not others.empty:
        st.markdown("📍 同じクラスターの他の時間帯：")
        for _, row in others.iterrows():
            st.markdown(f"- {row['曜日']} {row['開始時']}時台")
else:
    st.warning("該当するクラスタが見つかりませんでした。")
    
