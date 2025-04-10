import streamlit as st
from datetime import datetime #pip install streamlit-datetime-picker
import pandas as pd #pip install pandas
from supabase import create_client, Client #pip install streamlit supabase
import altair as alt

# Supabase 연결
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# 데이터 불러오기
def load_data():
    response = supabase.table("mmaconn").select("date").execute()
    return pd.DataFrame(response.data)

# Streamlit 앱 시작
st.subheader("📊 병역판정검사 QR앱 접속현황")

# 데이터 로드
df = load_data()

if df.empty:
    st.warning("데이터가 없습니다.")
else:
    # 값별로 개수 세기
    count_series = df["date"].value_counts()
    count_df = count_series.reset_index()
    count_df.columns = ["date", "count"]
    count_df.set_index("date", inplace=True)

    #st.write("📋 date 값별 건수:")
    #st.dataframe(count_df)

    # 기본 bar_chart로 시각화
    st.bar_chart(count_df)
