import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum


class Signal(Enum):
    BUY = 1,
    SELL = 2


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


def create_a_quote_plot(x_axis: np.ndarray, y_axis: np.ndarray, buy_sell_signals: np.ndarray,
                        macd_buy_sell_points: np.ndarray) -> None:
    line_width =1
    # plt.ion()
    plt.figure(figsize=(16, 9), dpi=100)
    plt.plot(x_axis, y_axis, linestyle="-", color="blue", label="Cena akcji", linewidth=line_width)

    new_cross_points = find_new_y_values_for_buy_sell_points(x_axis, y_axis, macd_buy_sell_points)

    plot_buy_sell_signals(buy_sell_signals, new_cross_points)

    plt.xlabel("Data")
    plt.ylabel("Cena [zł]")
    plt.title("Notowania giełdowe spółki PZU S.A. w okresie 04.01.2021 - 28.02.2025")
    plt.legend()
    # plt.show()
    filename = "pzu_notowania.jpg"
    plt.savefig(filename, dpi=800, bbox_inches="tight")
    print("Plot created")
    return


def find_new_y_values_for_buy_sell_points(x_axis: np.ndarray, y_axis: np.ndarray,
                                          macd_buy_sell_points: np.ndarray) -> np.ndarray:
    new_buy_sell_points = []
    index = 0
    for i in range(len(macd_buy_sell_points)):
        x = macd_buy_sell_points[i][0]
        for j in range(index + 1, len(x_axis)):
            if x_axis[j - 1] > x > x_axis[j]:
                index = j
                break
        y = y_axis[index - 1] + (
                (y_axis[index] - y_axis[index - 1]) * (x - x_axis[index - 1]) / (x_axis[index] - x_axis[index - 1]))
        new_buy_sell_points.append((x, y))
    return new_buy_sell_points


def create_macd_plot(y1_axis: np.ndarray, y2_axis: np.ndarray, x_axis: np.ndarray, buy_sell_signals: np.ndarray,
                     macd_buy_sell_points: np.ndarray) -> str:
    line_width = 1

    plt.figure(figsize=(16, 9), dpi=100)

    plt.plot(x_axis, y1_axis, linestyle="-", color="red", label="SIGNAL", linewidth=line_width)
    plt.plot(x_axis, y2_axis, linestyle="-", color="blue", label="MACD", linewidth=line_width)

    plot_buy_sell_signals(buy_sell_signals, macd_buy_sell_points)

    plt.xlabel("Data")
    plt.ylabel("Wartość")
    plt.title("Wykres MACD/SIGNAL spółki PZU S.A. w okresie 04.01.2021 - 28.02.2025")
    plt.legend()
    # plt.show()

    filename = "macd_pzu.jpg"
    plt.savefig(filename, dpi=800, bbox_inches="tight")
    print("Plot created")

    return filename


def plot_buy_sell_signals(buy_sell_signals, buy_sell_points):
    marker_size = 100
    buy_label_added = False
    sell_label_added = False
    for index, (x_intersection, y_intersection) in enumerate(buy_sell_points):
        if buy_sell_signals[index] == Signal.BUY:
            if not buy_label_added:
                plt.scatter(x_intersection, y_intersection, color='green', marker='^', s=marker_size,
                            label="Sygnał kupna")
                plt.text(x_intersection, y_intersection+0.3, round(y_intersection, 2), fontsize=12, ha='center', color='green')
                buy_label_added = True
            else:
                plt.scatter(x_intersection, y_intersection, color='green', marker='^', s=marker_size)
                plt.text(x_intersection, y_intersection+0.3, round(y_intersection, 2), fontsize=12, ha='center', color='green')
        else:
            if not sell_label_added:
                plt.scatter(x_intersection, round(y_intersection, 2), color='red', marker='v', s=marker_size,
                            label="Sygnał sprzedaży")
                plt.text(x_intersection, y_intersection-0.5, round(y_intersection, 2), fontsize=12, ha='center', color='red')
                sell_label_added = True
            else:
                plt.scatter(x_intersection, y_intersection, color='red', marker='v', s=marker_size)
                plt.text(x_intersection, y_intersection-0.5, round(y_intersection, 2), fontsize=12, ha='center', color='red')


def find_buy_sell_points(macd: np.ndarray, signal: np.ndarray, x_axis: np.ndarray):
    diff = macd - signal
    buy_sell_signals = []
    cross_points = []
    for i in range(1, len(diff)):
        if diff[i - 1] * diff[i] < 0:
            # Interpolacja liniowa między punktami i-1 i i
            x_intersection = x_axis[i - 1] - diff[i - 1] * (x_axis[i] - x_axis[i - 1]) / (diff[i] - diff[i - 1])
            y_intersection = macd[i - 1] + (macd[i] - macd[i - 1]) * (x_intersection - x_axis[i - 1]) / (
                    x_axis[i] - x_axis[i - 1])
            # Rozpoznanie kierunku przecięcia (od góry/od dołu)
            if macd[i - 1] > signal[i - 1] and macd[i] < signal[i]:
                buy_sell_signals.append(Signal.SELL)
            if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
                buy_sell_signals.append(Signal.BUY)
            cross_points.append((x_intersection, y_intersection))
    buy_sell_signals = np.array(buy_sell_signals)
    cross_points = np.array(cross_points)
    return buy_sell_signals, cross_points


def count_ema(data: np.ndarray, n: int) -> np.ndarray:
    alpha = 2 / (n + 1)  # współczynnik α
    decay_factors = (1 - alpha) ** np.arange(n + 1)  # wektor współczynników zaniku (1 - α)^i
    ema = np.nan * np.zeros_like(data)  # wektor wynikowy, początkowo wypełniony wartościami 0
    for i in range(len(data) - n):
        d = data[i:i + n + 1]  # notowania z ostatnich N+1 dni od i-tego dnia
        ema[i] = np.sum(d * decay_factors) / decay_factors.sum()  # EMA i-tego dnia
    return ema


def main():
    plt.ion()
    print("Program started")
    data = import_data("dane.csv")
    ema12 = count_ema(data[:, 1], 12)
    ema26 = count_ema(data[:, 1], 26)
    macd = ema12 - ema26
    signal = count_ema(macd, 9)
    buy_sell_signals, cross_points = find_buy_sell_points(macd, signal, data[:, 0])
    create_a_quote_plot(data[:, 0], data[:, 1], buy_sell_signals, cross_points)
    create_macd_plot(macd, signal, data[:, 0], buy_sell_signals, cross_points)
    plt.show


if __name__ == '__main__':
    main()
    print("Presss ENTER to exit")
    input()
