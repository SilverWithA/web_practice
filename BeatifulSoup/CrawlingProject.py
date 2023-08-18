import sys
import requests
from bs4 import BeautifulSoup
from newspaper import Article
from konlpy.tag import Okt
from collections import Counter
from collections import OrderedDict
import matplotlib
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from PIL import Image
import numpy as np


URL_BEFORE_KEYWORD = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query="
URL_BEFORE_PAGE_NUM = ("&sort=0&photo=0&field=0&pd=0&ds=&de=&cluster_rank=26&mynews=0&office_type=0"
                       "&office_section_code=0&news_office_checked=&nso=so:r,p:all,a:all&start=")

# 기사 제목 받아서 리스트 형식으로 반환하기(titles)
def get_link(keyword, page_range):
    link = []

    # (1) 반복문 사용해 페이지 크롤링
    for page in range(page_range):
        current_page = 1 + page * 10
        crawling_url = URL_BEFORE_KEYWORD + keyword + URL_BEFORE_PAGE_NUM + str(current_page)



        # Beatifulsoup으로 접근 가능한지 확인하기
        # 요청을 보내 정상적일 때만 확인하기
        response = requests.get(crawling_url)
        # print(response)  # 접근 가능 여부를 http 상태 코드 출력
        # 200출력 = 서버가 요청을 제대로 처리했음을 의미


        # 변수를 설정하여 내용 확인하기:BeatifulSoup 이용
        soup = BeautifulSoup(response.text,"lxml")  # html태그 불러옴:response.text
        # print(soup)                                       # html태그만 넘어옴 -> 구문분석을 통해 태그 추출
        url_tag = soup.select("a.news_tit") # a태그의 class가 news_tlt인 구문을 가져옴
        # print(url_tag)                      # 구문 긁히는 거 확인

        #href값을 원하는 것이기 때문에 list형태로 불러온 url_tag를 for문을 통해
        for url in url_tag:
            link.append(url["href"])

        # print("뉴스 기사 링크: ", link)
        return link
        
def get_article(file1,link):
    #파일로 저장
    # with open 사용하여 내용을 txt 파일로 저장하기
    with open(file1, "w",encoding="utf-8") as f:
        for i in link:
            article = Article(i, language="ko")  # Article 라이브러리 사용

            try:
                article.download()
                article.parse()  # 다운로드 후 파싱 -> 본문 가져오기 가능
            except:              # 에러가 있으면 continue
                continue

            news_title = article.title  # 뉴스 제목 가져오기
            news_content = article.text # 뉴스 내용 가져오기

            f.write(news_title)
            f.write(news_content)
        f.close()


# 단어 개수 세어보기
# file1은 내용이 담긴 txt
# file2 단어 개수를 담은 
def word_count(file1, file2):
    
    
    f = open(file1, "r", encoding="utf-8")  # 파일 불러오기
    g = open(file2, "w", encoding="utf-8")  # 파일 저장하기

    engine = Okt()   # konlp 라이브러리 사용
    data = f.read()  # 데이터 읽어오기
    all_nouns = engine.nouns(data)   # 데이터에서 명사 추출
    nouns = [n for n in all_nouns if(len(n)>1)]  # 길이가 1인 명사 지우기


    # 중복되는 명사 count 해주기
    count = Counter(nouns)  # Counter 클래스 사용하기- dictionary 형태로 저장함
    # 딕셔너리 형태인 count 정리하기:2중 for문을 이용하지 않고 OrderedDict 클래스 사용 -> 파이썬 3.6버전 이후로는 OrderedDict사용없이 sorted()만 사용해도 가능
    # Dicitonary = {key,value} - t[0]=key, t[1]=value
    by_num =OrderedDict(sorted(count.items(),key=lambda t: t[1],reverse=True))
    print(by_num)

    words = [i for i in by_num.keys()]
    number = [i for i in by_num.values()]

    for i,j in zip(words,number):
        final= f"{i}     {j}"
        g.write(final + '\n')

    f.close()
    g.close()

    return by_num,count

def full_vis_bar(by_num): # 그래프로 시각화하기: (1) 막대 그래프로 시각화


    # 일정 개수 미만은 삭제하여 시각화하기
    for w,n in list(by_num.items()):
        if n <= 15:
            del by_num[w]


    fig = plt.gcf()
    fig.set_size_inches(20,10)
    matplotlib.rc("font", family="Malgun Gothic", size=10)
    plt.title("기사에 등장한 단어 개수", fontsize=30)
    plt.xlabel("기사 등장 단어", fontsize=20)
    plt.ylabel("기사 등장 단어 개수", fontsize=20)


    #딕셔너리 형태의 by_num
    plt.bar(by_num.keys(), by_num.values())
    plt.xticks(rotation=45)
    plt.savefig("all_words.jpg")
    plt.show()

def top_n(count,file3):
    rank = count.most_common(10)
    g = open(file3,"w", encoding="utf-8")

    words = [i for i in dict(rank).keys()]
    number = [i for i in dict(rank).values()]

    for i,j in zip(words,number):
        final= f"{i}     {j}"
        g.write(final + '\n')

    g.close
    return rank


def top_n_plot(rank):
    top_n = dict(rank)
    fig = plt.gcf()
    fig.set_size_inches(20,10)
    matplotlib.rc("font", family="Malgun Gothic", size=10)
    plt.title("기사에 등장한 단어 개수 top 10", fontsize=30)
    plt.xlabel("기사 등장 단어", fontsize=20)
    plt.ylabel("기사 등장 단어 개수", fontsize=20)


    #딕셔너리 형태의 by_num
    plt.bar(top_n.keys(), top_n.values())
    plt.xticks(rotation=45)
    plt.savefig("tpo_n.jpg")
    plt.show()



# 워드클라우드 그리기
def word_cloud(by_num):

    # 이미지 파일에 덧씌우기
    masking_img = np.array(Image.open("alice_mask.png"))

    wc= WordCloud(font_path="malgun", background_color="white",
                  width=2500,
                  height=1500,
                  mask=masking_img)

    cloud = wc.generate_from_frequencies(by_num) #딕셔너리 형태 변수 입력해야함
    plt.imshow(cloud,interpolation="bilinear")
    plt.axis('off')
    plt.savefig('cloud.jpg')
    plt.show()


# argv란 띄어쓰기 기준으로 값을 받는 기능
def main(argv):
    link = get_link(argv[1], int(argv[2]))
    get_article("기사내용.txt",link)
    by_num,count = word_count("기사내용.txt", "word_count.txt")
    full_vis_bar(by_num)
    rank = top_n(count, "상위10위.txt")
    top_n_plot(rank)
    word_cloud(by_num)

# 네임 초기화 사용
if __name__ == "__main__":
    main(sys.argv)