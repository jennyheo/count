import streamlit as st
import pandas as pd #pip install pandas
from supabase import create_client, Client #pip install streamlit supabase

url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["service_key"]
supabase: Client = create_client(url, key)

def load_data():
    response = supabase.table("mmaconn").select("date").execute()
    return pd.DataFrame(response.data)
st.markdown("📊 병역판정검사 QR앱 접속 현황 ")
df = load_data()
if df.empty:
    st.warning("데이터가 없습니다.")
else:
    count_series = df["date"].value_counts().sort_index()
    pivot_df = pd.DataFrame({
        "count": count_series
    })
    st.dataframe(pivot_df)
    total_count = pivot_df["count"].sum()
    st.write(f"✅ 총 접속자: **{total_count}**")
