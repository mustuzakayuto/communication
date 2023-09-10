from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

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
    

if __name__ == "__main__":
    main('title')