import pandas
import requests
import json
import pandas as pd
import datetime
import pandas_ta as ta

def candlesusdt(symb, tf, p):
    url = 'https://fapi.binance.com/fapi/v1/klines'
    pare = symb + 'usdt'
    param = {'symbol': pare, 'interval': tf, 'limit': 1500}
    r = requests.get(url, params=param)
    if r.status_code == 200:
        df = pd.DataFrame(r.json())
        m = pd.DataFrame()
        m['date'] = df.iloc[:, 0].astype(float)
        m['date'] = pd.to_datetime(m['date'], unit='ms')
        m['open'] = df.iloc[:, 1].astype(float)
        m['high'] = df.iloc[:, 2].astype(float)
        m['low'] = df.iloc[:, 3].astype(float)
        m['close'] = df.iloc[:, 4].astype(float)
        m['ohlc4'] = (m['open'] + m['high'] + m['low'] + m['close'])/4  #Средняя цена закрытия
        m['volume_coin'] = df.iloc[:, 5].astype(float)
        m['volume_usdt'] = df.iloc[:, 6].astype(float)
        m['trades'] =m['volume_usdt']/df.iloc[:, 7].astype(float)
        m['volume_market_coin'] = df.iloc[:, 8].astype(float)*100/ m['volume_coin'] #skoko v % proslo po markety
        m['volume_market_usdt'] = df.iloc[:, 9].astype(float)
        m['sma'] = m['close'].rolling(p).mean() #Скользящая средняя
        m['sma_control'] = ta.sma(m['close'], length=p)  # Скользящая по периоду
        m['rsi'] = ta.rsi(m['close'], length=p)
        m['linreg'] = ta.linreg(m['close'], length=p) #Лин. регресия
        m['maxfor'] = m['high'].rolling(p).max() #Максимум за период
        m['minfor'] = m['low'].rolling(p).min() #Минимум за период

        m = m.dropna() #Убирает нули



        return m

        writer = pd.ExcelWriter('infa.xlsx', engine='xlsxwriter')
        m.to_excel(writer, 'Sheet1')
        writer.save()
    else:
        return print('Проверить исходные данные')


k = candlesusdt('btc', '5m', 100) # tyt menat ha hyznyu valyty + vremya
print(k)

# writer = pd.ExcelWriter('infa.xlsx', engine='xlsxwriter')
# k.to_excel(writer, 'Sheet1')
# #writer.save()