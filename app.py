import streamlit as st
from datetime import datetime, date

st.set_page_config(page_title="다중 D-Day 카운트다운", page_icon="📅", layout="wide")

st.title("📅 스마트 멀티 D-Day 카운트다운")
st.caption("중요한 일정들을 한눈에 모아보고 자유롭게 관리하세요.")

# 1. 세션 상태 초기화 (기본 D-Day 목록 제공)
if "dday_list" not in st.session_state:
    st.session_state.dday_list = [
        {"name": "2026 크리스마스", "date": date(2026, 12, 25)},
        {"name": "내년 새해", "date": date(2027, 1, 1)},
    ]

# 2. 사이드바: 새로운 D-Day 추가 양식
with st.sidebar:
    st.header("➕ 새 D-Day 추가")
    new_name = st.text_input("이벤트 이름", placeholder="예: 생일, 시험일")
    new_date = st.date_input("목표 날짜", value=date.today())
    
    if st.button("D-Day 등록하기", type="primary"):
        if new_name.strip():
            st.session_state.dday_list.append({"name": new_name, "date": new_date})
            st.success(f"'{new_name}' 추가 완료!")
            st.rerun()
        else:
            st.warning("이벤트 이름을 입력해주세요.")

st.divider()

# 3. 등록된 D-Day 목록 출력
if not st.session_state.dday_list:
    st.info("등록된 D-Day가 없습니다. 사이드바에서 새로 추가해보세요!")
else:
    # 2열(Grid) 형태로 카드 배치
    cols = st.columns(2)
    
    for idx, item in enumerate(st.session_state.dday_list):
        col = cols[idx % 2]
        
        with col:
            with st.container(border=True):
                target_datetime = datetime.combine(item["date"], datetime.min.time())
                now = datetime.now()
                
                time_diff = target_datetime - now
                days_left = time_diff.days
                total_seconds = int(time_diff.total_seconds())
                
                # 헤더 및 삭제 버튼
                c1, c2 = st.columns([4, 1])
                with c1:
                    st.subheader(f"📌 {item['name']}")
                    st.caption(f"목표일: {item['date'].strftime('%Y-%m-%d')}")
                with c2:
                    if st.button("삭제", key=f"del_{idx}"):
                        st.session_state.dday_list.pop(idx)
                        st.rerun()
                
                # D-Day 계산 결과
                if total_seconds > 0:
                    hours = (total_seconds % (24 * 3600)) // 3600
                    minutes = (total_seconds % 3600) // 60
                    
                    st.metric(label="남은 시간", value=f"D-{days_left}")
                    st.info(f"⏳ **{days_left}일 {hours}시간 {minutes}분** 남음")
                elif days_left == 0 and total_seconds <= 0:
                    st.success("🎉 오늘이 D-Day입니다!")
                else:
                    st.metric(label="지나온 시간", value=f"D+{abs(days_left)}")
                    st.warning(f"지나간 이벤트 ({abs(days_left)}일 경과)")
