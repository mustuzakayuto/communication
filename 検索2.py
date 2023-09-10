import openpyxl
import time
from selenium import webdriver

#googleで検索する文字
search_string = '猫 喋る なぜ'

#Seleniumを使うための設定とgoogleの画面への遷移
INTERVAL = 2.5
URL = "https://www.google.com/"
driver_path = "./chromedriver-win64/"
driver = webdriver.Chrome(executable_path=driver_path)
driver.maximize_window()
time.sleep(INTERVAL)
driver.get(URL)
time.sleep(INTERVAL)

#文字を入力して検索
driver.find_element_by_name('q').send_keys(search_string)
driver.find_elements_by_name('btnK')[1].click() #btnKが2つあるので、その内の後の方
time.sleep(INTERVAL)

#検索結果の一覧を取得する
results = []
flag = False
while True:
    g_ary = driver.find_elements_by_class_name('g')
    for g in g_ary:
        result = {}
        result['url'] = g.find_element_by_class_name('yuRUbf').find_element_by_tag_name('a').get_attribute('href')
        result['title'] = g.find_element_by_tag_name('h3').text
        results.append(result)
        if len(results) >= 50: #抽出する件数を指定
            flag = True
            break
    if flag:
        break
    driver.find_element_by_id('pnnext').click()
    time.sleep(INTERVAL)

#ワークブックの作成とヘッダ入力
workbook = openpyxl.Workbook()
sheet = workbook.active
sheet['A1'].value = 'タイトル'
sheet['B1'].value = 'URL'

#シートにタイトルとURLの書き込み
for row, result in enumerate(results, 2):
    sheet[f"A{row}"] = result['title']
    sheet[f"B{row}"] = result['url']

workbook.save(f"google_search_{search_string}.csv")
driver.close()