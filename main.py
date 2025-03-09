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


def create_plot(data: np.ndarray, x: int, y: int) -> None:
    y_axis = data[:, y]
    x_axis = data[:, x]
    plt.figure(figsize=(15, 5), dpi=800)
    plt.plot(x_axis, y_axis, linestyle="-", color="b", label="Cena")
    plt.xlabel("Data")
    plt.ylabel("Kwota")
    plt.title("Ceny akcji spółki PZU S.A.")
    plt.legend()
    plt.grid(True)
    plt.savefig("ceny_pzu.png", dpi=800, bbox_inches="tight")
    plt.show()
    return


def count_ema(data: np.ndarray, n: int) -> np.ndarray:
    alpha = 2 / (n + 1)  # współczynnik α
    factors = (1 - alpha) ** np.arange(n + 1)  # wektor czynników [1, (1-α), (1-α)^2, (1-α)^3, ..., (1-α)^N]
    factors = factors[::-1]  # odwrócenie wektora tak, aby czynniki dla najświeżyszch danych były największe
    ema = np.zeros_like(data)  # wektor wynikowy, początkowo wypełniony zerami
    for i in range(n, len(data)):
        ema[i] = np.sum(data[i - n:i + 1] * factors) / factors.sum()
    return ema


def main():
    data = import_data("Historyczne ceny PZU.csv")
    macd = count_ema(data[:, 1], 12) - count_ema(data[:, 1], 26)
    signal = count_ema(macd, 9)
    print(macd)


if __name__ == '__main__':
    main()
