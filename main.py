import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("영화의 **날짜별 일관객 변화**를 그래프로 살펴봅니다.")

DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    numeric_columns = [
        "순위",
        "영화코드",
        "일관객",
        "누적관객",
        "스크린수",
        "상영횟수"
    ]

    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

df = load_data()

st.info(
    f"📊 데이터 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}  |  "
    f"총 {len(df):,}개의 기록"
)

st.header("📈 그래프 1. 영화별 날짜에 따른 일관객 변화")

st.write(
    "영화를 하나 선택하면 해당 영화의 날짜별 일관객 변화를 확인할 수 있습니다."
)

movie_list = sorted(df["영화명"].dropna().unique())

selected_movie = st.selectbox(
    "🎬 영화를 선택하세요",
    movie_list
)

movie_df = df[df["영화명"] == selected_movie].copy()
movie_df = movie_df.sort_values("날짜")

fig = px.line(
    movie_df,
    x="날짜",
    y="일관객",
    markers=True,
    title=f"「{selected_movie}」 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수"
    }
)

fig.update_traces(
    hovertemplate=
    "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
    "<b>일관객</b>: %{y:,}명"
    "<extra></extra>"
)

fig.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified"
)

st.plotly_chart(fig, use_container_width=True)

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 한 문장으로 작성하세요.",
    placeholder="예: 주말에 일관객 수가 증가하고 평일에는 감소하는 경향을 볼 수 있다.",
    height=80,
    key="graph1_comment"
)

st.divider()

st.header("📊 그래프 2. 다음 그래프")
st.info("여기에 두 번째 그래프를 추가할 예정입니다.")

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 2의 특징을 한 문장으로 작성하세요.",
    placeholder="그래프를 추가한 후 알게 된 내용을 한 문장으로 작성하세요.",
    height=80,
    key="graph2_comment"
)

st.divider()

st.header("📊 그래프 3. 다음 그래프")
st.info("여기에 세 번째 그래프를 추가할 예정입니다.")

st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 3의 특징을 한 문장으로 작성하세요.",
    placeholder="그래프를 추가한 후 알게 된 내용을 한 문장으로 작성하세요.",
    height=80,
    key="graph3_comment"
)

with st.expander("🔎 원본 데이터 일부 보기"):
    st.dataframe(
        df.head(20),
        use_container_width=True
    )
