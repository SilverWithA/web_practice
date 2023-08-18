from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("http://shshop.testy.kr/")
time.sleep(2)

elem = driver.find_element(By.NAME, "sch_text")
time.sleep(2)


# # 문자열 전달(입력) 명령 실행
# elem.send_keys("티셔츠")
# elem.send_keys(Keys.RETURN) # enter키 입력
# time.sleep(2)
#
#
# ## 상품 티셔츠 제목만 가져오기
# searchList = driver.find_elements(By.CLASS_NAME, "goods_name")
# for i in searchList:
#     print(i.text)
#
# driver.close()



# 패션의류라는 링크로 들어감 - 패션의류에 딱히 class나 name 속성 X:LINK_TEXT 이용 -> 클릭 작동(X)
# driver.find_elements(By.LINK_TEXT, "패션의류")
# time.sleep(2)


# 대안(1) driver.get()으로 직접 링크 지정
driver.get("http://shshop.testy.kr/shop/goods_list.php?cate_id=1")

# CSS로 찾기
categorySearch = driver.find_element(By.CSS_SELECTOR, "input.input_box150")
categorySearch.send_keys("자켓")
driver.find_elements(By.CLASS_NAME," button_small")[1].click()

driver.close()