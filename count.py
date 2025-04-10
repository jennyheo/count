import streamlit as st
import pandas as pd #pip install pandas
import altair as alt
from supabase import create_client, Client #pip install streamlit supabase
st.set_page_config(
     page_title="QR앱접속현황"
     , page_icon="📊"
)
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["service_key"]
supabase: Client = create_client(url, key)

def load_data():
    response = supabase.table("mmaconn").select("date").execute()
    return pd.DataFrame(response.data)
st.subheader("📊 병역판정검사 QR앱 접속 현황 ", divider=True)
df = load_data()
if df.empty:
    st.warning("데이터가 없습니다.")
else:
    count_series = df["date"].value_counts().sort_index()
    pivot_df = pd.DataFrame({
        "날짜": count_series.index,
        "접속자 수": count_series.values
    })
    total_count = pivot_df["접속자 수"].sum()
    st.write(f"✅ 총 접속자: **{total_count}**")

    # 📋 표 출력
    st.dataframe(pivot_df.set_index("날짜"))

    # ✅ 가로 막대 차트 그리기 (Altair)
    chart = alt.Chart(pivot_df).mark_bar().encode(
        x=alt.X("접속자 수:Q"),
        y=alt.Y("날짜:N", sort="-x"),  # 날짜 기준 역순 정렬
        tooltip=["날짜", "접속자 수"]
    ).properties(
        width=600,
        height=400,
        #title="📅 날짜별 접속자"
    )

    st.altair_chart(chart, use_container_width=True)
    
