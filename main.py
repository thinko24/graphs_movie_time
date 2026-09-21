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
# 그래프 3. 날짜별 TOP 10 일관객 합계 (영역 그래프)
# =========================================================
st.divider()

st.header("📊 그래프 3. 날짜별 TOP 10 일관객 합계 추이")
st.write(
    "매일 **박스오피스 상위 10개 영화의 일관객 합계**를 산출하여 극장가의 전체적인 활성도를 영역 그래프로 보여줍니다."
)

# 1. 날짜별 10위권(순위 <= 10) 데이터 필터링 후 합계 계산
top10_daily = (
    df[df["순위"] <= 10]
    .groupby("날짜", as_index=False)["일관객"]
    .sum()
    .sort_values("날짜")
)

# 2. 일관객 합계 상위 3일 추출
top3_days = top10_daily.sort_values("일관객", ascending=False).head(3)

# 3. 영역 그래프(Area chart) 생성
fig3 = px.area(
    top10_daily,
    x="날짜",
    y="일관객",
    title="날짜별 TOP 10 영화 일관객 합계 추이 (영역 그래프)",
    labels={
        "날짜": "날짜",
        "일관객": "TOP 10 일관객 합계(명)"
    }
)

fig3.update_traces(
    line_color="#1f77b4",
    hovertemplate=
    "<b>날짜</b>: %{x|%Y-%m-%d}<br>"
    "<b>TOP 10 일관객 합계</b>: %{y:,}명"
    "<extra></extra>"
)

# 4. 관객수 상위 3일 위치에 주석(Annotations) 및 마커 추가
for idx, row in top3_days.reset_index().iterrows():
    date_str = row["날짜"].strftime("%Y-%m-%d")
    val = row["일관객"]

    # 상위 3일 포인트 표시 (붉은색 점)
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[val],
        mode="markers",
        marker=dict(color="red", size=9),
        showlegend=False,
        hoverinfo="skip"
    )

    # 텍스트 주석 추가
    fig3.add_annotation(
        x=row["날짜"],
        y=val,
        text=f"<b>TOP {idx+1}</b><br>{date_str}<br>({val:,.0f}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowcolor="red",
        ax=0,
        ay=-45,
        bordercolor="red",
        borderwidth=1,
        borderpad=4,
        bgcolor="rgba(255, 255, 255, 0.8)",
        opacity=0.9
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="TOP 10 일관객 합계(명)",
    hovermode="x unified"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# 상위 3일 정보 요약 표시
st.caption("🏆 **TOP 10 일관객 합계가 가장 컸던 TOP 3 날짜**")
top3_display = top3_days.copy()
top3_display["날짜"] = top3_display["날짜"].dt.strftime("%Y-%m-%d")
top3_display["일관객"] = top3_display["일관객"].map(lambda x: f"{x:,}명")
top3_display.columns = ["날짜", "TOP 10 총 관객 수"]
top3_display.index = [1, 2, 3]
st.dataframe(top3_display, use_container_width=True)


st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 3의 특징을 한 문장으로 작성하세요.",
    placeholder="예: 특정 연휴나 주말에 TOP 10 영화의 총 관객수가 크게 집중되는 모습을 볼 수 있다.",
    height=80,
    key="graph3_comment"
)


# =========================================================
# 그래프 4. 흥행 TOP 10 영화 및 10위권 차트인 날수 (가로 막대)
# =========================================================
st.divider()

st.header("📊 그래프 4. 흥행 TOP 10 영화 및 10위권 진입 날수")
st.write(
    "기간 동안 **총 일관객 수가 많은 상위 10개 영화**를 가로 막대그래프로 비교합니다. "
    "막대에 마우스를 올리면 해당 영화가 **10위권(TOP 10)에 든 일수(날수)**를 함께 볼 수 있습니다."
)

# 1. 영화별 총 일관객 합계 및 10위권(순위 <= 10) 차트인 날수 계산
movie_summary = (
    df[df["순위"] <= 10]
    .groupby("영화명", as_index=False)
    .agg(
        총일관객=("일관객", "sum"),
        차트인날수=("날짜", "nunique")
    )
    .sort_values("총일관객", ascending=False)
    .head(10)
)

# 2. Plotly 가로 막대그래프 생성을 위해 순서 정렬
movie_summary_sorted = movie_summary.sort_values("총일관객", ascending=True)

fig4 = px.bar(
    movie_summary_sorted,
    x="총일관객",
    y="영화명",
    orientation="h",
    title="기간 내 총 일관객 수 TOP 10 영화",
    labels={
        "총일관객": "총 일관객 수(명)",
        "영화명": "영화명",
        "차트인날수": "10위권 진입 날수"
    },
    text_auto=",.0f",
    color="총일관객",
    color_continuous_scale="Blues",
    hover_data={"차트인날수": True, "총일관객": ":,"}
)

fig4.update_traces(
    hovertemplate=
    "<b>영화명</b>: %{y}<br>"
    "<b>총 일관객 수</b>: %{x:,}명<br>"
    "<b>10위권 진입 날수</b>: %{customdata[0]}일"
    "<extra></extra>"
)

fig4.update_layout(
    xaxis_title="총 일관객 수(명)",
    yaxis_title="영화명",
    coloraxis_showscale=False,
    height=500
)

st.plotly_chart(
    fig4,
    use_container_width=True
)


st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 4의 특징을 한 문장으로 작성하세요.",
    placeholder="예: 총 관객 수가 비슷한 영화라도 10위권 내 상영 날수에는 큰 차이가 나타날 수 있다.",
    height=80,
    key="graph4_comment"
)


# =========================================================
# 그래프 5. 월×요일별 일관객 합계 히트맵
# =========================================================
st.divider()

st.header("🔥 그래프 5. 월×요일별 일관객 합계 (히트맵)")
st.write(
    "각 **월과 요일의 조합에 따른 총 일관객 수**를 히트맵으로 시각화합니다. "
    "색이 **진할수록** 해당 월·요일의 관객 수 합계가 많음을 의미합니다."
)

# 1. 월 및 요일 파생변수 생성
df_heatmap = df.copy()
df_heatmap["월"] = df_heatmap["날짜"].dt.month.astype(str) + "월"
df_heatmap["요일_code"] = df_heatmap["날짜"].dt.dayofweek  # 월:0 ~ 일:6

weekday_names = ["월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일"]
df_heatmap["요일"] = df_heatmap["요일_code"].map(lambda x: weekday_names[x])

# 2. 월 및 요일 순서 보정을 위한 Pivot 테이블 생성
# 행: 월, 열: 요일(월~일 순서)
heatmap_pivot = df_heatmap.pivot_table(
    index="월",
    columns="요일",
    values="일관객",
    aggfunc="sum"
).fillna(0)

# 월 정렬 (1월~12월 순서 유지)
months_order = [f"{m}월" for m in range(1, 13) if f"{m}월" in heatmap_pivot.index]
heatmap_pivot = heatmap_pivot.reindex(index=months_order, columns=weekday_names)

# 3. Plotly Heatmap 생성
fig5 = px.imshow(
    heatmap_pivot,
    labels=dict(x="요일", y="월", color="일관객 합계"),
    x=weekday_names,
    y=heatmap_pivot.index,
    color_continuous_scale="Purples",  # 관객이 많을수록 진한 보라색
    text_auto=",.0f",
    title="월×요일별 일관객 합계 히트맵"
)

fig5.update_traces(
    hovertemplate=
    "<b>월</b>: %{y}<br>"
    "<b>요일</b>: %{x}<br>"
    "<b>일관객 합계</b>: %{z:,}명"
    "<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월",
    height=550
)

st.plotly_chart(
    fig5,
    use_container_width=True
)


st.subheader("📝 이 그래프로 알 수 있는 것")

st.text_area(
    "그래프 5의 특징을 한 문장으로 작성하세요.",
    placeholder="예: 특정 월의 주말(토·일)에 관객수가 크게 몰리는 경향을 한눈에 파악할 수 있다.",
    height=80,
    key="graph5_comment"
)


# =========================================================
# 데이터 확인
# =========================================================
with st.expander("🔎 원본 데이터 일부 보기"):
    st.dataframe(
        df.head(20),
        use_container_width=True
    )
