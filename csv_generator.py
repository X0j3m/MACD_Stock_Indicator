import numpy as np
import pandas as pd

# Generowanie przykładowych danych
np.random.seed(42)

# Liczba dni
n_days = 30

# Generowanie przykładowych danych: cena zamknięcia w dniu (w tym przypadku losowa wartość)
dates = pd.date_range(start="2025-02-01", periods=n_days, freq='D')
closing_prices = np.random.uniform(50, 60, size=n_days)  # Losowe ceny z zakresu 50-60

# Tworzenie DataFrame
data = pd.DataFrame({
    "Data": dates,
    "Ostatnio": closing_prices
})

# Funkcja do obliczania EMA
def count_ema(data: np.ndarray, n: int) -> np.ndarray:
    alpha = 2 / (n + 1)  # współczynnik α
    ema = np.empty_like(data)
    ema[:n] = np.nan  # Wartości początkowe EMA są ustawione na NaN
    
    # Pierwsza wartość EMA to średnia z pierwszych N dni
    ema[n-1] = np.mean(data[:n])
    
    # Obliczenie EMA dla reszty danych
    for i in range(n, len(data)):
        ema[i] = alpha * data[i] + (1 - alpha) * ema[i-1]
    
    return ema

# Obliczanie EMA12 i EMA26
ema12 = count_ema(data["Ostatnio"].values, 12)
ema26 = count_ema(data["Ostatnio"].values, 26)

# Dodanie wyników EMA do DataFrame
data["EMA12"] = ema12
data["EMA26"] = ema26

# Wyświetlenie wyników
data.head()
