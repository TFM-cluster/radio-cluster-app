import streamlit as st
import pandas as pd

# データ読み込み
df = pd.read_csv("cluster_by_time.csv")

# タイトル
st.title("📻 ラジオAI：時間帯クラスタ診断")

# 曜日と時間の入力
weekdays = sorted(df["曜日"].unique())
weekday = st.selectbox("📅 曜日を選んでください", weekdays)
hour = st.slider("🕒 時間を選んでください（24h形式, 5〜29）", min_value=5, max_value=29, value=9)

# 該当時間のクラスタを表示
row = df[(df["曜日"] == weekday) & (df["開始時"] == hour)]

if not row.empty:
    cluster = int(row["代表クラスタ"].values[0])
    st.success(f"✅ {weekday}曜 {hour}時台 は『クラスタ {cluster}』です")

    # 同じクラスタの他の時間帯を抽出（今の時間以外）
    others = df[(df["代表クラスタ"] == cluster) & ~((df["曜日"] == weekday) & (df["開始時"] == hour))]

    if not others.empty:
        st.markdown("📍 同じクラスタの他の時間帯：")
        for _, r in others.iterrows():
            st.write(f"・{r['曜日']}曜 {r['開始時']}時台")
    else:
        st.info("このクラスタの他の時間帯は見つかりませんでした。")
else:
    st.error("この時間帯のデータが存在しません。")
