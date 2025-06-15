import requests
from datetime import datetime
import pytz

def fetch_weather_data(url):
    """
    日本気象庁の天気予報データを取得する。
    Args:
        url (str): 気象庁のJSONデータURL
    Returns:
        dict: 取得したJSONデータ、失敗時はNone
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # HTTPエラーチェック
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"データ取得エラー: {e}")
        return None
    except ValueError as e:
        print(f"JSONパースエラー: {e}")
        return None

def format_date(iso_date):
    """
    ISO形式の日付を 'YYYY年MM月DD日' 形式に変換。
    Args:
        iso_date (str): ISO形式の日付（例: 2025-06-15T12:00:00+0900）
    Returns:
        str: フォーマット済みの日付（例: 2025年06月15日）
    """
    try:
        dt = datetime.fromisoformat(iso_date.replace("Z", "+0000"))
        return dt.astimezone(pytz.timezone("Asia/Tokyo")).strftime("%Y年%m月%d日")
    except ValueError as e:
        print(f"日付フォーマットエラー: {e}")
        return iso_date

def display_chiba_nw_forecast(data):
    """
    千葉県南部の天気予報を表示する。
    Args:
        data (dict): 気象庁のJSONデータ
    """
    if not data:
        print("データが取得できませんでした。")
        return

    try:
        time_series = data[0]["timeSeries"][0]
        for area in time_series["areas"]:
            if area["area"]["name"] == "南部":
                print("\n千葉県南部の天気予報")
                print("=" * 20)
                for date, weather in zip(time_series["timeDefines"], area["weathers"]):
                    formatted_date = format_date(date)
                    weather = weather.strip()  # 余分な空白を削除
                    print(f"{formatted_date} の天気: {weather}")
                
                # 降水確率の表示（データがある場合）
                if "pops" in area:
                    print("\n降水確率")
                    print("-" * 20)
                    for date, pop in zip(time_series["timeDefines"], area["pops"]):
                        formatted_date = format_date(date)
                        print(f"{formatted_date} の降水確率: {pop}%")
    except (KeyError, IndexError) as e:
        print(f"データ処理エラー: {e}")

def main():
    url = "https://www.jma.go.jp/bosai/forecast/data/forecast/120000.json"
    data = fetch_weather_data(url)
    display_chiba_nw_forecast(data)

if __name__ == "__main__":
    main()

