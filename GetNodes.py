"""
某人的小脚本
目前支持的网站：
    1、v2raya.com
    2、clashnode.cc
这两个基本上就涵盖了网上能找到的绝大多数节点（非github)
"""

from lxml import etree
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import base64
import datetime
import time
import sys
import pytz
import sys


# -- init -- #
# 可调参数
TRY_LIM = 10 # 获取内容尝试次数

# browse
headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}
targets = []

driver_out = '''
--- 选择浏览器 ---
[1] - Microsoft Edge
[2] - Firefox
[3] - Google Chrome
'''

# driver = input(driver_out)
driver = sys.argv[1] if len(sys.argv) > 1 else '3'

print(driver)
if driver == '1':
    edge_options = webdriver.EdgeOptions()
    edge_options.add_argument('--headless')  # 无头模式

    # 反自动化检测
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    edge_options.add_experimental_option('useAutomationExtension', False)

    # 大量的优化
    edge_options.add_argument('--disable-gpu')
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-infobars')
    edge_options.add_argument('--disable-notifications')
    edge_options.add_argument('--ignore-certificate-errors')
    edge_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Edge(options = edge_options)
elif driver == '2':
    firefox_options = webdriver.FirefoxOptions()
    firefox_options.add_argument('--headless')  # 无头模式
    firefox_options.add_argument('--disable-gpu')
    firefox_options.add_argument('--ignore-certificate-errors')
    firefox_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Firefox(options = firefox_options)
elif driver == '3':
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')  # 无头模式

    # 反自动化检测
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)

    # 大量的优化
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-notifications')
    chrome_options.add_argument('--ignore-certificate-errors')
    chrome_options.add_argument('--ignore-ssl-errors')
    driver = webdriver.Chrome(options = chrome_options)
else:
    print('啊？什么意思？')
    input('按下回车以退出...')
    sys.exit()


# files
input_file = "urls.txt"


# -- -- #

# Get time
lt = time.localtime(time.time())
tz = pytz.timezone("Asia/Shanghai")
now = datetime.datetime.now(tz)
formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
update_time = "## Update Time: " + formatted_time + "\n```\n"
tm_mon = str(lt.tm_mon) if lt.tm_mon >= 10 else '0'+str(lt.tm_mon)
tm_mday = str(lt.tm_mday) if lt.tm_mday >= 10 else '0'+str(lt.tm_mday)


# Get share urls
# Supported: clashnode.cc, v2raya.com
print("Get share urls...")

# 1、freeclashnode.com
# https://node.clashnode.cc/uploads/2025/01/0-20250121.txt
for i in range(1, 5):
    tmp = 'https://node.clashnode.cc/uploads/{0}/{1}/{3}-{0}{1}{2}.txt'.format(lt.tm_year, tm_mon, tm_mday, i)
    targets.append(tmp)
print("freeclashnode.com Finished!")

# 2、v2raya.com
web_url = 'https://v2raya.net/free-nodes/free-v2ray-node-subscriptions.html'
# /html/body/div[2]/main/div[1]/article/div/ul/li[7]/text()[2]
# https://www.v2raya.net/free-nodes/free-v2ray-node-subscriptions.html
driver.get(web_url)
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/article/div/ul/li[13]"))
)
html = driver.page_source
selector = etree.HTML(html)
for i in range(1, 14):
    tmp = selector.xpath(f'/html/body/div[2]/main/div[1]/article/div/ul/li[{i}]/text()[2]')
    # print(tmp)
    tmp = tmp[0].strip()
    if tmp != '':
        targets.append(tmp)

print("v2raya.com Finished!")
    
for i in targets: print(i)
# sys.exit(0)

# Input share urls
'''
with open(input_file, "r", encoding="utf-8") as f:
    oglt = f.read()

oglt = oglt.strip()
flag = False
target = ''
for i in range(len(oglt)-1):
    if oglt[i] == oglt[i+1] == '\n' and not flag:
        target = target + oglt[i]
        flag = True
    elif oglt[i] == '\n' and oglt[i+1] != '\n' and flag:
        flag = False
    elif not flag:
        target += oglt[i]

targets = target.split('\n')
'''


# Get share content
print("Get share content...")
urls = ""
j = 0
for op in targets:
    print(j, j / len(targets) * 100)
    j += 1

    CONNECTION_RESET = False

    # 使用 selenium 获取订阅链接内容
    try_cnt = 1
    while try_cnt <= TRY_LIM:
        try:
            driver.get(op)
        except Exception as e:
            print('[ERROR]', e)

            if str(e).find('ERR_CONNECTION_RESET') != -1:
                CONNECTION_RESET = True
                break

            print('尝试次数：', try_cnt)
            print('重试...')
            time.sleep(1)
        else:
            try_cnt = TRY_LIM + 25
            content = driver.find_element(By.TAG_NAME, "body").text

    if CONNECTION_RESET:
        print('连接错误：')
        print(op)
        print('连接被重置，跳过此链接\n')
        continue

    # 对于未编码内容 - 直接加仓
    if content.find(':') != -1:
        urls += content
        continue

    # 对于b64编码 - 解码加仓
    # base64 解码填充
    pad_num = len(content) % 4
    content = content[:len(content)-pad_num]
    
    # base 64 解码
    add_ctt = base64.b64decode(content).decode('unicode_escape')

    urls += add_ctt

urls_lst = list(set(urls.split('\n')))
urls = ""
for i in urls_lst:
    i = i.strip()
    if i != '':
        urls += i + '\n'
urls = urls[:-1]

# B64 encode
urls = urls.encode()
urls = base64.b64encode(urls).decode('unicode_escape')

with open("index.html", "w", encoding='utf-8') as f:
    f.write(urls)
    print("index.html 已生成！")

urls = update_time + urls + "\n\n```"

print(urls[:25])

with open("README.md", "w", encoding='utf-8') as f:
    f.write(urls)
    print("README.md 已生成！")
