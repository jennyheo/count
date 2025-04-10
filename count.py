import streamlit as st
from datetime import datetime #pip install streamlit-datetime-picker
import pandas as pd #pip install pandas
from supabase import create_client, Client #pip install streamlit supabase

# Supabase 연결
url = st.secrets["supabase"]["url"]
key = st.secrets["supabase"]["key"]
supabase: Client = create_client(url, key)

# Supabase 클라이언트 생성
#supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
today=datetime.now().strftime("%Y%m%d")
#st.write(today)

#세션당 1번씩 기록
# if "visited" not in st.session_state:
#     st.session_state.visited=True
#     supabase.table("mmaconn").insert ({"date":today}).execute()

# #통계가져오기
response=supabase.table("mmaconn").select("date").execute()
records=response.data

df=pd.DataFrame(records)
# count_by_date=df["date"].value_counts().sort_index()

st.title("접속자수")
# st.bar_chart(count_by_date)
st.dataframe(df)


# 오늘 날짜
today_str = datetime.now().strftime("%Y%m%d")


# 세션 상태 확인 (중복 인서트 방지)
if "visited_today" not in st.session_state:
    st.session_state.visited_today = False

if not st.session_state.visited_today:
    # Supabase에서 오늘 날짜에 대한 기록 확인
    response = supabase.table("mmaconn").select("date").eq("date", today_str).execute()

    if response and not response.data:
        # 오늘 날짜에 해당하는 기록이 없으면 삽입
        insert_response = supabase.table("mmaconn").insert({"date": today_str}).execute()
        if insert_response.error:
            st.error(f"저장 오류: {insert_response.error.message}")
        else:
            st.session_state.visited_today = True
    else:
        st.session_state.visited_today = True

response = supabase.table("mmaconn").select("date").execute()

if response.data:
    df = pd.DataFrame(response.data)

    # 총 접속자 수
    total_visits = len(df)

    # 오늘 접속자 수
    today_visits = (df["date"] == today_str).sum()

    # 결과 출력
    st.metric("총 접속자 수", total_visits)
    st.metric("오늘 접속자 수", today_visits)

else:
    st.warning("데이터가 없습니다.")
    st.text(f"에러: {response.error}")
