import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def import_data(filename: str) -> np.ndarray:
    try:
        # pobranie danych z pliku
        data = pd.read_csv(filename, usecols=["Data", "Ostatnio", "Otwarcie", "Max.", "Min."])
    except FileNotFoundError:
        exit("File not found")
    except ValueError:
        exit("Invalid data format")

    # zamiana daty z formatu str na typ daty
    data["Data"] = pd.to_datetime(data["Data"], format="%d.%m.%Y")
    # zamiana wartości wejściowych z formatu str na float
    data["Ostatnio"] = data["Ostatnio"].str.replace(',', '.').astype(float)
    data["Otwarcie"] = data["Otwarcie"].str.replace(',', '.').astype(float)
    data["Max."] = data["Max."].str.replace(',', '.').astype(float)
    data["Min."] = data["Min."].str.replace(',', '.').astype(float)

    # zapisanie danych w formacie macierzy numpy
    data = data.to_numpy()
    return data

def create_macd_plot(macd: np.ndarray, signal: np.ndarray, x_axis: np.ndarray) -> str:
    lw = 0.2
    plt.figure(figsize=(15, 9), dpi=1500)

    y1_axis = macd
    y2_axis = signal
    plt.plot(x_axis, y1_axis, linestyle="-", color="r", label="SIGNAL", linewidth=lw)
    plt.plot(x_axis, y2_axis, linestyle="-", color="b", label="MACD", linewidth=lw)


    plt.xlabel("Data")
    plt.title("Wykres MACD spółki PZU S.A.")
    plt.legend()

    filename = "macd_pzu.pdf"
    plt.savefig(filename, dpi=800, bbox_inches="tight")
    print("Plot created")

    return filename


def count_ema(data: np.ndarray, n: int) -> np.ndarray:
    alpha = 2 / (n + 1)  # współczynnik α
    decay_factors = (1 - alpha) ** np.arange(n + 1)  # wektor współczynników zaniku (1 - α)^i
    ema = np.nan * np.zeros_like(data)  # wektor wynikowy, początkowo wypełniony wartościami NaN
    for i in range(len(data) - n):
        d = data[i:i + n + 1]  # notowania z ostatnich N+1 dni od i-tego dnia
        ema[i] = np.sum(d * decay_factors) / decay_factors.sum()  # EMA i-tego dnia
    return ema


def main():
    data = import_data("Historyczne ceny PZU.csv")
    ema12 = count_ema(data[:, 1], 12)
    ema26 = count_ema(data[:, 1], 26)
    macd = ema12 - ema26
    signal = count_ema(macd, 9)
    create_macd_plot(macd, signal, data[:, 0])


if __name__ == '__main__':
    main()
