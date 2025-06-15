import requests

APP_ID = "edbb2603f4c37c41e608bdd93a2a2af1ba2dae12"
API_URL  = "https://api.e-stat.go.jp/rest/3.0/app/json/getStatsData"


params = {
    "appId": APP_ID,
    "statsDataId": "0003036792",  # 消費者物価指数（CPI）に変更
    "cdArea": "01000",  # 全国（CPIは地域別データの例）
    "cdTime": "2020000000",  # 2020年
    "lang": "J",  # 日本語を指定
    "sectionHeaderFlg": "1"  # ヘッダー情報を含める
}

response = requests.get(API_URL, params=params)
data = response.json()
print(data)