import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from scipy import stats

def crypto_analysis(symbol):
    # Binance API'sinden verileri çek
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}USDT&interval=1d"
    response = requests.get(url)
    data = response.json()
    
    # Verileri pandas dataframe'ine dönüştür
    df = pd.DataFrame(data, columns=['Open time', 'Open', 'High', 'Low', 'Close', 'Volume', 'Close time', 'Quote asset volume', 'Number of trades', 'Taker buy base asset volume', 'Taker buy quote asset volume', 'Ignore'])
    df = df.astype({'Open time': int, 'Open': float, 'High': float, 'Low': float, 'Close': float, 'Close time': int})
    
    # Tarihleri datetime formatına dönüştür
    df['Open time'] = pd.to_datetime(df['Open time'], unit='ms')
    df['Close time'] = pd.to_datetime(df['Close time'], unit='ms')
    
    # Günlük değişim oranını hesapla
    df['daily_change'] = df['Close'].pct_change()
    
    # Histogram oluştur
    plt.hist(df['daily_change'], bins=50)
    plt.xlabel('Günlük Değişim Oranı')
    plt.ylabel('Sayı')
    plt.title(f"{symbol} Kripto Para Günlük Değişim Oranı")
    plt.show()
    
    # Ortalama ve standart sapma hesapla
    mean = np.mean(df['daily_change'])
    std = np.std(df['daily_change'])
    
    # Risk analizi için döviz çiftinin fiyatının çeyreklik volatilite oranını hesapla
    rolling_volatility = df['daily_change'].rolling(window=90).std().mean()
    
    # Tavsiye ver
    if mean > 0 and std < rolling_volatility and mean / std > stats.t.ppf(0.95, len(df['daily_change'])-1):
        print(f"{symbol} kripto para yatırım yapılması için uygun bir seçenektir.")
    else:
        print(f"{symbol} kripto para yatırım yapılması için uygun bir seçenek değildir.")


# Örnek bir kripto para sembolü
symbol = "GALA"
crypto_analysis(symbol)
