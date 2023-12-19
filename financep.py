import streamlit as st
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# Veri çekme ve işleme
@st.cache
def load_data(symbol, start, end):
    data = yf.download(symbol, start=start, end=end)
    return data

# Ana kod
def main():
    st.title('Hisse Senedi Analiz Aracı')

    # Kullanıcı girişleri
    start_date = st.sidebar.date_input("Başlangıç Tarihi", value=pd.to_datetime('2022-01-01'))
    end_date = st.sidebar.date_input("Bitiş Tarihi", value=pd.to_datetime('today'))
    selected_stock = st.sidebar.selectbox("Hisse Senedi Seçin", ['AAPL', 'GOOG', 'MSFT', 'AMZN'])

    data = load_data(selected_stock, start_date, end_date)

    # Hisse Senedi Fiyat Grafiği
    st.subheader('Hisse Senedi Fiyat Grafiği')
    st.line_chart(data['Close'])

    # Günlük Getiri Grafiği
    st.subheader('Hisse Senedi Günlük Getiri Grafiği')
    daily_return = data['Adj Close'].pct_change()
    st.line_chart(daily_return)

    # Hareketli Ortalama
    st.subheader('Hareketli Ortalama')
    ma_days = st.slider('Hareketli Ortalama Gün Sayısı Seçin', 5, 100, 20)
    ma = data['Adj Close'].rolling(window=ma_days).mean()
    st.line_chart(ma)

    # Korelasyon
    st.subheader('Hisse Senedi Korelasyonu')
    corr = data[['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume']].corr()
    sns.heatmap(corr, annot=True)
    st.pyplot()

    # Risk ve Beklenen Getiri Analizi
    st.subheader('Risk ve Beklenen Getiri Analizi')
    rets = data['Adj Close'].pct_change()
    area = (rets.mean(), rets.std())
    plt.scatter(rets.mean(), rets.std())
    plt.xlabel('Beklenen Getiri')
    plt.ylabel('Risk')
    st.pyplot()

if __name__ == "__main__":
    main()
