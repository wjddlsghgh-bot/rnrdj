import streamlit as st
from datetime import date, datetime

# 웹 페이지 기본 설정
st.set_page_config(page_title="D-Day 계산기", page_icon="📅")

st.title("📅 D-Day 계산기")
st.write("목표 날짜를 선택하거나 입력하여 남은 일수를 확인하세요.")

# 사용자가 직접 날짜와 이벤트 이름을 선택할 수 있는 입력창
event_name = st.text_input("이벤트 이름", value="크리스마스")
target_date = st.date_input("목표 날짜", value=date(2026, 12, 25))

# D-Day 계산
today = date.today()
diff = (target_date - today).days

st.divider()

# 결과 출력
if diff > 0:
    st.metric(label=f"{event_name}까지", value=f"D-{diff}")
    st.info(f"오늘부터 {diff}일 남았습니다!")
elif diff == 0:
    st.balloons()
    st.success(f"🎉 오늘은 {event_name} D-Day입니다!")
else:
    st.metric(label=f"{event_name}로부터", value=f"D+{abs(diff)}")
    st.warning(f"{event_name}로부터 {abs(diff)}일 지났습니다.")
