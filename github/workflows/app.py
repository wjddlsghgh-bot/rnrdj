import streamlit as st
from datetime import datetime, date
import time

st.set_page_config(page_title="스마트 D-Day 카운트다운", page_icon="⏳", layout="centered")

st.title("⏳ 실시간 D-Day 카운트다운")
st.caption("중요한 일정과 남은 시간을 한눈에 확인하세요.")

# 1. 사용자 입력 부분
col1, col2 = st.columns(2)
with col1:
    event_name = st.text_input("📌 이벤트 이름", value="2026 크리스마스")
with col2:
    target_date = st.date_input("📅 목표 날짜", value=date(2026, 12, 25))

# 2. 날짜 및 실시간 시간 계산
target_datetime = datetime.combine(target_date, datetime.min.time())
now = datetime.now()

time_diff = target_datetime - now
days_left = time_diff.days
total_seconds = int(time_diff.total_seconds())

st.divider()

# 3. D-Day 메인 메트릭 출력
if total_seconds > 0:
    hours = (total_seconds % (24 * 3600)) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    st.metric(label=f"[{event_name}] 까지 남은 시간", value=f"D-{days_left}")
    
    # 실시간 상세 카운트다운 카드
    st.subheader("⏱️ 상세 카운트다운")
    st.info(f"👉 **{days_left}일 {hours}시간 {minutes}분 {seconds}초** 남았습니다!")

    # 진행률 표시 (올해 기준 예시)
    start_of_year = datetime(now.year, 1, 1)
    total_period = (target_datetime - start_of_year).total_seconds()
    passed_period = (now - start_of_year).total_seconds()
    progress = max(0.0, min(1.0, passed_period / total_period)) if total_period > 0 else 0
    
    st.write("📊 목표까지의 올해 달성도")
    st.progress(progress)

elif days_left == 0 and total_seconds <= 0:
    st.balloons()
    st.success(f"🎉 축하합니다! 오늘은 **{event_name}** D-Day입니다!")
else:
    st.metric(label=f"[{event_name}] 로부터 지나온 시간", value=f"D+{abs(days_left)}")
    st.warning(f"이미 {abs(days_left)}일이 경과한 이벤트입니다.")
