import jieba
import requests
from bs4 import BeautifulSoup

# 文本提取
def extract_text(url):
    """Extract html content."""
    page_source = requests.get(url).content
    bs_source = BeautifulSoup(page_source)
    report_text = bs_source.find_all('p')

    text = ''

    for p in report_text:
        text += p.get_text()
        text += '\n'

    return text

# 利用jieba分词，并计算词频
def word_frequency(text):
    from collections import Counter

    words = [word for word in jieba.cut(text, cut_all=True) if len(word) >= 2]
    c = Counter(words)

    for word_freq in c.most_common(10):
        word, freq = word_freq
        print(word, freq)

url_2016 = 'http://www.gov.cn/guowuyuan/2016-03/05/content_5049372.htm'
text_2016 = extract_text(url_2016)
word_frequency(text_2016)