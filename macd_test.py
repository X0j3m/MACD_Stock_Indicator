import pandas as pd
import matplotlib.pyplot as plt

# Wczytanie danych z pliku CSV
data = pd.read_csv('dane.csv')

# Sprawdzenie pierwszych kilku wierszy w celu weryfikacji danych
print("Pierwsze wiersze danych:")
print(data.head())

# Zmiana formatu daty
data['Data'] = pd.to_datetime(data['Data'], format='%d.%m.%Y')

# Zamiana przecinków na kropki w kolumnach liczbowych
data['Ostatnio'] = data['Ostatnio'].str.replace(',', '.').astype(float)

# Funkcja do usuwania jednostek i konwersji kolumny "Wol." na wartości numeryczne
def convert_volume(volume):
    if 'M' in volume:
        return float(volume.replace('M', '').replace(',', '.')) * 1e6
    elif 'K' in volume:
        return float(volume.replace('K', '').replace(',', '.')) * 1e3
    return float(volume.replace(',', '.'))

# Przekształcenie kolumny "Wol." na wartości numeryczne
data['Wol.'] = data['Wol.'].apply(convert_volume)

# Sprawdzamy, czy kolumna "Ostatnio" zawiera liczby
print("\nPodstawowe informacje o danych:")
print(data[['Data', 'Ostatnio', 'Wol.']].head())

# Obliczenie MACD (12-dniowa EMA - 26-dniowa EMA)
data['EMA12'] = data['Ostatnio'].ewm(span=12, adjust=False).mean()
data['EMA26'] = data['Ostatnio'].ewm(span=26, adjust=False).mean()

# Obliczenie MACD jako różnica EMA12 i EMA26
data['MACD'] = data['EMA12'] - data['EMA26']

# Obliczenie linii SIGNAL (9-dniowa EMA MACD)
data['SIGNAL'] = data['MACD'].ewm(span=9, adjust=False).mean()

# Sprawdzamy, czy MACD i SIGNAL zostały poprawnie obliczone
print("\nMACD i SIGNAL:")
print(data[['Data', 'MACD', 'SIGNAL']].head())

# Rysowanie wykresu
plt.figure(figsize=(12, 6))
plt.plot(data['Data'], data['MACD'], label='MACD', color='blue')
plt.plot(data['Data'], data['SIGNAL'], label='SIGNAL', color='red')
plt.fill_between(data['Data'], data['MACD'] - data['SIGNAL'], color='gray', alpha=0.3)
plt.title('Wykres MACD i SIGNAL')
plt.xlabel('Data')
plt.ylabel('Wartość')
plt.legend(loc='best')
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
