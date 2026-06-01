from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import datetime

# 깃허브 가상 서버(화면 없음)를 위한 브라우저 설정
chrome_options = Options()
chrome_options.add_argument("--headless") # 화면 없이 백그라운드 실행
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080")

print("로봇 브라우저를 시동합니다...")
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

try:
    # 1. 풋몹(FotMob) 데이터 접속 테스트
    print("풋몹에 접속 중...")
    driver.get("https://www.fotmob.com/")
    time.sleep(5) # 로딩 대기
    fotmob_data = driver.page_source[:1000] # 일단 잘 들어갔는지 앞부분만 확보

    # 2. K리그 데이터포털 접속 테스트
    print("K리그 데이터포털 접속 중...")
    driver.get("https://data.kleague.com/")
    time.sleep(5)
    kleague_data = driver.page_source[:1000]

    # 오늘 날짜로 파일 저장
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    filename = f"football_data_{today}.txt"
    
    with open(filename, "w", encoding="utf-8") as f:
        f.write("=== FotMob Data ===\n")
        f.write(fotmob_data + "\n\n")
        f.write("=== K-League Data ===\n")
        f.write(kleague_data + "\n")
        
    print(f"수집 성공! {filename} 파일이 생성되었습니다.")

except Exception as e:
    print(f"오류 발생: {e}")

finally:
    driver.quit()
