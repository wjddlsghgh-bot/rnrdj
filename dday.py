import os
from datetime import datetime, date

def calculate_dday(target_date_str):
    """
    YYYY-MM-DD 형식의 문자열을 받아 오늘 기준 D-Day를 계산합니다.
    """
    today = date.today()
    target_date = datetime.strptime(target_date_str, "%Y-%m-%d").date()
    
    diff = (target_date - today).days
    
    if diff > 0:
        return f"D-{diff}"
    elif diff == 0:
        return "D-Day 🎉"
    else:
        return f"D+{abs(diff)}"

if __name__ == "__main__":
    # 환경 변수에서 목표 날짜와 제목을 가져오거나 기본값을 사용합니다.
    target_date = os.getenv("TARGET_DATE", "2026-12-25")
    title = os.getenv("EVENT_TITLE", "크리스마스")
    
    dday_result = calculate_dday(target_date)
    print(f"[{title}] {target_date}까지 남은 기간: {dday_result}")
    
    # GitHub Action 환경변수(GITHUB_OUTPUT)에 결과를 저장하여 다음 단계에서 사용할 수 있도록 합니다.
    github_output = os.getenv("GITHUB_OUTPUT")
    if github_output:
        with open(github_output, "a", encoding="utf-8") as f:
            f.write(f"dday_text=[{title}] {dday_result}\n")
