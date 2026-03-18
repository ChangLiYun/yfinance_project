import yfinance as yf
from pprint import pprint

def stock_info(id):
    tick = yf.Ticker(id)
    info = tick.info
    print(f'公司名稱{info.get("shortName")}')
    print(f'最新訊息{info.get("message")}')
    print(f'今日市場均價{info.get("regularMarketPrice")}')
    print(f'今年度EPS{info.get("priceEpsCurrentYear")}')
    print(f'今日行情{info.get("regularMarkDayRange")}')

stock_info("2330.TW")