from textblob import TextBlob
import 翻訳

def main2():
    # テキストデータを入力
    conversation_text = """
    今日の天気は最高ですね！
    でも、昨日は雨が降っていて嫌な日でした。
    明日は友達とピクニックに行く予定です！

    """

    # 文章を分割
    sentences = conversation_text.split("\n")
    dataList=[]
    for txt in sentences:
        txt=txt.strip()
        if txt!="":
            dataList.append(txt)
        
    SENTENCES = dataList
    print(sentences)
    翻訳語list=[]
    for i,txt in enumerate(sentences):
        txt=txt.strip()
        if txt !="":
            
            # print(txt)
            text= 翻訳.main(txt)
            # print(text)
            # sentences[i]=text
            翻訳語list.append(text)
    print(翻訳語list)
    sentences = 翻訳語list
    pos=[]
    scoreList=[]
    pos2=[]
    scoreList2=[]
    # 各文の感情極性を評価し、ポジティブな文を特定
    positive_sentences = []
    negative_sentences = []
    for i,sentence in enumerate(sentences):
        print(i)
        if sentence:
            analysis = TextBlob(sentence)
            sentiment_score = analysis.sentiment.polarity
            # print(sentiment_score)
            if sentiment_score > 0:
                pos.append(i)
                scoreList.append(sentiment_score)
                positive_sentences.append(sentence)
            elif sentiment_score < 0:
                pos2.append(i)
                scoreList2.append(sentiment_score)
                negative_sentences.append(sentence)
                

    # ポジティブな文を表示
    if positive_sentences:
        print("ポジティブな文:")
        
        for index,score in zip(pos,scoreList):
            print("スコア: "+str(score))
            print(index)
            print(SENTENCES[index])
    else:
        print("ポジティブな文は見つかりませんでした。")
    print("---------------")
    if negative_sentences:
        print("ネガティブな文:")
        for index,score in zip(pos2,scoreList2):
            print("スコア: "+str(score))
            print(index)
            print(SENTENCES[index])
    else:
        print("ネガティブな文は見つかりませんでした。")
def main(TXT):
    txt = 翻訳.main(TXT)
    Is_positive = False

    if txt:
        analysis = TextBlob(txt)
        sentiment_score = analysis.sentiment.polarity
        print(sentiment_score)
        if sentiment_score > 0:
            Is_positive=True
    return sentiment_score,Is_positive

main2()