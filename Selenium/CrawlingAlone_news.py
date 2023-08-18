from collections import Counter, OrderedDict

import pandas as pd
from konlpy.tag import Okt
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from newspaper import Article
from selenium.webdriver.common.action_chains import ActionChains
import time
import pandas as od



driver = webdriver.Chrome()
driver.get("https://www.naver.com/")
time.sleep(2)


elem = driver.find_element(By.XPATH, '//*[@id="query"]')

# search_keyword = input("뉴스를 수집할 키워드를 입력해주세요: ")
elem.send_keys("초당옥수수")
time.sleep(2)

# 엔터
elem.send_keys(Keys.RETURN)
time.sleep(2)

# 뉴스 탭으로 이동
driver.find_element(By.XPATH, '//*[@id="lnb"]/div[1]/div/ul/li[8]/a').click()
print("뉴스 탭을 클릭했습니다.")
time.sleep(2)



# 뉴스 기사 url 수집 ----------------------------------------
def get_url(search_page):
    links = []

    for page in range(1,search_page+1):

        # 페이지 이동
        page_path = '//*[@id="main_pack"]/div[2]/div/div/a[' + str(page) + ']'
        driver.find_element(By.XPATH, page_path).click()
        # print(f"현재 {page}번째 페이지에 있습니다.")

        # 요소 가져오기
        something = driver.find_elements(By.CLASS_NAME,"news_tit")
        for i in something:
            links.append(i.get_attribute("href"))

    return links

# 뉴스 기사 제목 및 내용 수집 - Airticle 라이브러리 사용 ----------------------------------------
def get_article(links):
    news_titles = []
    news_contents = []

    for link in links:
        article = Article(link, language="ko")

        try:
            article.download()
            article.parse()  # 다운로드 후 파싱 -> 본문 가져오기 가능
        except:
            continue

        news_titles.append(article.title)
        news_contents.append(article.text)

    return news_titles, news_contents

# get_article(get_url(2))

# 뉴스 기사 빈발 top5 단어 반환 -----------------------------------
def count_word(news_contents):

    words_list = []

    engine = Okt()  # konlp 라이브러리 사용
    for news_content in news_contents:
        all_nouns = engine.nouns(news_content)  # news_content에서 명사 추출
        nouns = [n for n in all_nouns if (len(n) > 1)]  # 길이가 1인 명사 지우기

        # 명사 추출
        count = Counter(nouns)
        top_5 = count.most_common(5)
        # words_list.append((dict(top_5).keys()))
        words_list.append(list(dict(top_5).keys()))

    return words_list




# 실행 해보기------------------------------
search_pages = int(input("수집할 페이지수를 입력해주세요: "))
url = get_url(search_pages)
titles, contents = get_article(url)
top_5 = count_word(contents)


# # csv 파일로 저장 ------------------------------------------------
df = pd.DataFrame({"제목":titles,"내용":contents,"기사 url":url,"단어 5가지":top_5})
print(df)
df.to_csv("초당옥수수2.csv", index = False, encoding="utf-8")




driver.close()