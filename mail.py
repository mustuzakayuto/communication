import json
import requests
import time
def main(mail_address,subject,message):
    url = "https://script.google.com/macros/s/AKfycbzLAtNM-0Vaq4mUVPwf7ofUZj537Lc6jZUiQ3QD-EquQfZdrRziYut_34hDyvLnkR4PZA/exec"
    # JSON形式でデータを用意してdataに格納
    data = {
        "recipient": mail_address,
        "subject" : subject,
        "body" : message
    }
    # json.dumpでデータをJSON形式として扱う
    r = requests.post(url, data=json.dumps(data))
    print(r)
