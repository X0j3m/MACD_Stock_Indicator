import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
def load_data(filename):
    df = pd.read_csv(filename, delimiter=',', decimal=',', dtype=str)  # Wczytaj wszystko jako stringi
    df = df[::-1]  # Odwrócenie kolejności, aby dane były od najstarszych do najnowszych
    df["Ostatnio"] = df["Ostatnio"].str.replace(',', '.').astype(float)  # Zamiana przecinków na kropki i konwersja
    return df


# Obliczanie MACD i Signal
def calculate_macd(df):
    short_ema = df['Ostatnio'].ewm(span=12, adjust=False).mean()
    long_ema = df['Ostatnio'].ewm(span=26, adjust=False).mean()
    df['MACD'] = short_ema - long_ema
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

# Znalezienie punktów kupna i sprzedaży
def find_signals(df):
    buy_signals = [None]  # Pierwszy element brak sygnału
    sell_signals = [None]  # Pierwszy element brak sygnału
    
    for i in range(1, len(df)):
        if df['MACD'][i] > df['Signal'][i] and df['MACD'][i - 1] <= df['Signal'][i - 1]:
            buy_signals.append(df['Ostatnio'][i])
            sell_signals.append(None)
        elif df['MACD'][i] < df['Signal'][i] and df['MACD'][i - 1] >= df['Signal'][i - 1]:
            sell_signals.append(df['Ostatnio'][i])
            buy_signals.append(None)
        else:
            buy_signals.append(None)
            sell_signals.append(None)

    df['Buy'] = buy_signals
    df['Sell'] = sell_signals


# Rysowanie wykresu MACD i cen akcji
def plot_macd_and_prices(df):
    fig, (ax1, ax2) = plt.subplots(2, figsize=(12, 8), sharex=True)
    
    # Wykres cen akcji
    ax1.plot(df['Data'], df['Ostatnio'], label='Cena', color='blue')
    ax1.scatter(df['Data'], df['Buy'], label='Kupno', marker='^', color='green', alpha=1)
    ax1.scatter(df['Data'], df['Sell'], label='Sprzedaż', marker='v', color='red', alpha=1)
    ax1.legend()
    ax1.set_title('Notowania giełdowe')
    
    # Wykres MACD
    ax2.plot(df['Data'], df['MACD'], label='MACD', color='black')
    ax2.plot(df['Data'], df['Signal'], label='Signal', color='red')
    ax2.legend()
    ax2.set_title('MACD i Signal')
    
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Główna funkcja
if __name__ == "__main__":
    filename = "Historyczne ceny PZU.csv"  # Zmień na właściwą nazwę pliku
    df = load_data(filename)
    calculate_macd(df)
    find_signals(df)
    plot_macd_and_prices(df)
