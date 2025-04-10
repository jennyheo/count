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

@st.cache_data
def load_data():
    response = supabase.table("mmaconn").select("date").execute()
    data = response.data
    df = pd.DataFrame(data)

    # 문자열 date 기준으로 그룹화
    df_count = df.groupby('date').size().reset_index(name='count')
    df_count = df_count.sort_values('date')  # 문자열 정렬
    return df_count

st.subheader("📊 병역판정검사 QR앱 접속 현황 ", divider=True)

df_count = load_data()
total_count = df_count['count'].sum()
st.markdown(f" 🧮 총 접속자 수: **{total_count}명**")

st.dataframe(df_count, use_container_width=True)

# st.bar_chart는 index를 x축으로 사용하므로, date를 index로 설정
df_chart = df_count.set_index('date')
st.bar_chart(df_chart)

