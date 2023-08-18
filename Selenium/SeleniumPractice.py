from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()

# get() -> 페이지로 이동
driver.get("http://www.python.org")
time.sleep(5)


# find_element(): html 요소를 찾는 함수 - Name의 속성이 q인 속성
# 검색창의 요소가 name="q" 임
# 요소가 복수일시: find_elements형태로 리스트로 받아오기 가능
elem = driver.find_element(By.NAME, "q")
time.sleep(5)

elem.clear()
time.sleep(5)
# 문자열 전달(입력) 명령 실행
elem.send_keys("pycon")

# enter키 입력
elem.send_keys(Keys.RETURN)
time.sleep(5)


driver.close()