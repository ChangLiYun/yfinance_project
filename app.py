import pymssql
import numpy
import yfinance as yf
from pprint import pprint
import schedule
import time


server = "wenrene.database.windows.net"
database= "free-sql-db-1116192" 
user = "dbeng" 
password = "Re2521026"


def stock_info_30s(id):
    # --- A. 抓取資料 ---
    tick = yf.Ticker(id)
    info = tick.info
    
    # 擷取要存入資料庫的欄位
    # .get() 可預防 None
    symbol = id
    open_p = info.get("open")
    last_p = info.get("currentPrice") # yfinance 目前建議用 currentPrice
    high_p = info.get("dayHigh")
    low_p = info.get("dayLow")

    #--- B. 連接資料庫並執行 SQL ---
    try:
        # 1. 登入 azure sql sever
        connect = pymssql.connect(server, database, user, password)
        print('db登入成功')

        # 2. 透過該物件(Connection)產生一個 Cursor物件負責執行 SQL 語法
        cursor = connect.cursor()
        print("cursor取得成功")

        # 3. 透過 cursor 將 sql 送給 azure sql server 執行
        cursor.execute('''
                            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='StockData' AND xtype='U')
                            CREATE TABLE StockData (
                                ID INT IDENTITY(1,1) PRIMARY KEY,
                                Symbol NVARCHAR(10),
                                OpenPrice FLOAT,
                                LastPrice FLOAT,
                                DayHigh FLOAT,
                                DayLow FLOAT,
                                UpdateTime DATETIME DEFAULT GETDATE() 
                            )
                        ''')
        # 4. 取得查詢結果 
        insert_sql = """
            INSERT INTO StockData (Symbol, OpenPrice, LastPrice, DayHigh, DayLow) 
            VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(insert_sql, (symbol, open_p, last_p, high_p, low_p))
         
        # 5. 存檔 (Commit)
        connect.commit()
        print(f"--- 成功寫入Azure SQL ---")

    except  Exception as e:
        print(f"發生錯誤: {e}")

    finally: 
        cursor.close()
        connect.close()
#----主程式------------------------------------------------------
# 設定結束或取消的方式
# 抓開盤時間:9:00~ 13:00 每30秒一次
schedule.every(30).seconds.do(stock_info_30s, id="2330,TW").until("13:30")

#檢查並執行所有已到時間的任務
while True:
    schedule.run_pending()
    time.sleep(1)





# stock_info("3037.TW")
#------------------------------------

# def ticker_summary(id):
#     tick = yf.Ticker(id)
#     info = tick.fast_info
#     #print( info )   # 今日最高最低 開盤/收盤 目前行情
#     print("fast_info 通常會與即時狀況有時間差")
#     print(f'開盤: {info.open}')
#     print(f'今日最高: {info.day_high}')
#     print(f'今日最低: {info.day_low}')
#     print(f'目前價格: {info.last_price}')

# print("------------- TSMC -------------")
# ticker_summary("2330.TW")
# print("------------- 欣興-------------")
# ticker_summary("3037.TW")
#---------------------------------------------------
# def stock_info(id):
#     tick = yf.Ticker(id)
#     info = tick.info
#     print(f'公司名稱{info.get("shortName")}')
#     print(f'最新訊息{info.get("message")}')
#     print(f'今日市場均價{info.get("regularMarketPrice")}')
#     print(f'今年度EPS{info.get("priceEpsCurrentYear")}')
#     print(f'今日行情{info.get("regularMarkDayRange")}')   
