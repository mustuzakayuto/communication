from bs4 import BeautifulSoup
import requests
import pandas as pd
import time
import urllib.parse
def main(keyword="None"):
    

    url = 'https://kino-code.work/?s={}'.format(keyword)

    r = requests.get(url)
    time.sleep(3)

    soup = BeautifulSoup(r.text,'html.parser')
    page_na = soup.find(class_="pagination")

    # Check if the 'pagination' element exists before attempting to find page numbers
    if page_na:
        page_num = page_na.find_all(class_="page-numbers")
        pages = [i.text for i in page_num]
    else:
        # If 'pagination' element is not found, assume there is only one page
        pages = ['1']

    urls = []

    for page in pages:
        url = 'https://kino-code.work/?s={}&paged={}'.format(keyword, page)
        urls.append(url)

    links = []
    titles = []
    snippets = []

    for url in urls:
        r = requests.get(url)
        time.sleep(3)
        soup = BeautifulSoup(r.text, 'html.parser')
        get_list_info = soup.find_all("a", class_="entry-card-wrap")

        for item in get_list_info:
            get_list_link = item.attrs.get('href', '')
            links.append(get_list_link)

            get_list_title = item.attrs.get('title', '')
            titles.append(get_list_title)

            get_list_snippet = item.find(class_="entry-card-snippet")
            if get_list_snippet:
                snippets.append(get_list_snippet.text)
            else:
                snippets.append('')

    result = {
        'title': titles,
        'link': links,
        'snippet': snippets
    }
    print(len(titles))
    # df = pd.DataFrame(result)
    # df.head(10)
    # df.to_csv('result.csv', index=False, encoding='utf-8')
    print(result)

    
    return result
def main2(query):


    # Google検索のURLを構築
    url = f"https://www.google.com/search?q={query}"
    
    # HTTP GETリクエストを送信
    response = requests.get(url)
    
    # レスポンスが成功（ステータスコード200）の場合
    if response.status_code == 200:
        # BeautifulSoupを使ってHTMLを解析
        
        soup = BeautifulSoup(response.text, 'html.parser')
        # print(soup)
        # タイトルとリンクを取得
        # search_results = []
        
        
        titlelist=[]
        linklist=[]
        
        # for search_result in soup.find_all('a'):
        #     linklist.append(search_result['href'])
            # print(search_result)
        for search_result in soup.find_all('h3'):
            decoded_link=None
            parent_link = search_result.find_parent('a')
            
            if parent_link:
                link = parent_link.get("href", "")
                # Decode the URL and then remove unwanted parts
                decoded_link = urllib.parse.unquote(link)
                print(decoded_link)
                if "/url?q=" in decoded_link:
                    decoded_link=decoded_link.split("/url?q=")[1]
                if "&sa=" in decoded_link:
                    decoded_link = decoded_link.split("&sa=")[0]
                # print(decoded_link)
                # Remove any additional parameters after the last "/"
                # if "%" in decoded_link or "&" in decoded_link:
                #     decoded_link = decoded_link.rsplit('/', 1)[0]
                if "http" in decoded_link:
                    linklist.append(decoded_link)
                else :
                    decoded_link=None
                    parent_link=None
            # decoded_link = decoded_link.rsplit('/', 1)[0]
            titlelist.append(search_result.text)
            if decoded_link==None:
                
                if parent_link==None:
                    titlelist.pop()
                else:
                    linklist.append(parent_link)
            # search_results.append({'title': search_result.text,"link":decoded_link})
        result = {
            'title': titlelist,
            'link': linklist
        }
        return result
    else:
        print("Google検索に失敗しました。")
def main3():
    url="https://twitter.com/explore/tabs/trending"
    response = requests.get(url)
    
    # レスポンスが成功（ステータスコード200）の場合
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        for search_result in soup.find_all('span'):
            
            print(search_result)
        
if __name__ == "__main__":
    # main('title')
    # data=main2("")
    # for i in data:
    #     print(i)
    #     print(data[i])
    main3()
    # "css-901oao css-16my406 r-poiln3 r-bcqeeo r-qvutc0"

    