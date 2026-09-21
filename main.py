import streamlit as st
import pandas as pd
import plotly.express as px


# =========================================================
# 기본 설정
# =========================================================
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("영화의 **날짜별 일관객 변화**를 그래프로 살펴봅니다.")


# =========================================================
# 데이터 불러오기
# =========================================================
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 날짜를 진짜 날짜 형식으로 변환
    df["날짜"] = pd.to_datetime(
        df["날짜"].astype(str),
        format="%Y%m%d"
    )

    # 숫자형 데이터 변환
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


# =========================================================
# 데이터 기본 정보
# =========================================================
st.info(
    f"📊 데이터 기간: {df['날짜'].min().strftime('%Y-%m-%d')} ~ "
    f"{df['날짜'].max().strftime('%Y-%m-%d')}  |  "
    f"총 {len(df):,}개의 기록"
)


# =========================================================
# 그래프 1
# =========================================================
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

st.plotly_chart(
    fig,
    use_container_width=True
)


# =========================================================
# 그래프 1 해석
# =========================================================
st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 한 문장으로 작성하세요.",
    placeholder="예: 주말에 일관객 수가 증가하고 평일에는 감소하는 경향을 볼 수 있다.",
    height=80,
    key="graph1_comment"
)


# =========================================================
# 그래프 2
# =========================================================
st.divider()

st.header("📈 그래프 2. 일관객 합계가 가장 큰 영화 5편 비교")

st.write(
    "전체 기간 동안의 **일관객 합계가 가장 큰 영화 5편**을 골라 "
    "날짜별 일관객 변화를 한 그래프에서 비교합니다."
)

# 영화별 전체 기간 일관객 합계 계산
top5_movies = (
    df.groupby("영화명", as_index=False)["일관객"]
    .sum()
    .sort_values("일관객", ascending=False)
    .head(5)
)

top5_names = top5_movies["영화명"].tolist()

# 상위 5편만 날짜별 데이터로 추출
top5_df = df[df["영화명"].isin(top5_names)].copy()
top5_df = top5_df.sort_values(["날짜", "영화명"])

fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    markers=True,
    title="일관객 합계 상위 5편의 날짜별 일관객 변화",
    labels={
        "날짜": "날짜",
        "일관객": "일관객 수",
        "영화명": "영화"
    },
    hover_data={
        "영화명": True,
        "날짜": "|%Y-%m-%d",
        "일관객": ":,"
    }
)

fig2.update_traces(
    hovertemplate=
    "<b>영화</b>: %{fullData.name}<br>"
    "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
    "<b>일관객</b>: %{y:,}명"
    "<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일관객 수(명)",
    hovermode="x unified",
    legend_title="영화",
    legend=dict(
        itemclick="toggle",
        itemdoubleclick="toggleothers"
    )
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.caption(
    "💡 그래프 오른쪽 범례의 영화 이름을 클릭하면 해당 영화의 선을 켜거나 끌 수 있습니다. "
    "두 번 클릭하면 해당 영화만 볼 수 있습니다."
)


# 그래프 2의 전체 기간 일관객 합계
with st.expander("🏆 일관객 합계 상위 5편 확인"):
    ranking_df = top5_movies.copy()
    ranking_df["일관객"] = ranking_df["일관객"].map(lambda x: f"{x:,}명")
    ranking_df.index = range(1, len(ranking_df) + 1)
    ranking_df.index.name = "순위"
    st.dataframe(
        ranking_df,
        use_container_width=True
    )


# =========================================================
# 그래프 2 해석
# =========================================================
st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프에서 발견한 특징을 한 문장으로 작성하세요.",
    placeholder="예: 영화마다 개봉 이후 일관객 수의 변화 양상이 서로 다르게 나타난다.",
    height=80,
    key="graph2_comment"
)


# =========================================================
# 그래프 3을 위한 구역
# =========================================================
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


# =========================================================
# 데이터 확인
# =========================================================
with st.expander("🔎 원본 데이터 일부 보기"):
    st.dataframe(
        df.head(20),
        use_container_width=True
    )
