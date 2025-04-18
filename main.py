import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from enum import Enum


class Signal(Enum):
    BUY = 1
    SELL = 2


class TransactionResult(Enum):
    PROFIT = 2
    LOSS = 1


def import_data(filename: str) -> np.ndarray:
    try:
        # pobranie danych z pliku
        data = pd.read_csv(filename, usecols=["Data", "Ostatnio"])
    except FileNotFoundError:
        exit("File not found")
    except ValueError:
        exit("Invalid data format")

    # zamiana daty z formatu str na typ daty
    data["Data"] = pd.to_datetime(data["Data"], format="%d.%m.%Y")
    # zamiana wartości wejściowych z formatu str na float
    data["Ostatnio"] = data["Ostatnio"].str.replace(',', '.').astype(float)

    # zapisanie danych w formacie macierzy numpy
    data = data.to_numpy()
    return data


def create_a_quote_plot(x_axis: np.ndarray, y_axis: np.ndarray, buy_sell_signals: np.ndarray,
                        macd_buy_sell_points: np.ndarray) -> None:
    line_width = 1
    # plt.ion()
    plt.figure(figsize=(16, 9), dpi=100)
    plt.plot(x_axis, y_axis, linestyle="-", color="blue", label="Cena akcji", linewidth=line_width)

    new_cross_points = find_new_axis_values_for_buy_sell_points(x_axis, y_axis, macd_buy_sell_points)

    plot_buy_sell_signals(buy_sell_signals, new_cross_points, False, False)

    plt.xlabel("Data")
    plt.ylabel("Cena [zł]")
    plt.title("Notowania giełdowe spółki PZU S.A. w okresie 04.01.2021 - 28.02.2025")
    plt.legend()
    plt.grid(True)
    # plt.show()
    filename = "pzu_notowania.jpg"
    # plt.savefig(filename, dpi=800, bbox_inches="tight")
    print("Plot created")
    return


def find_new_axis_values_for_buy_sell_points(x_axis: np.ndarray, y_axis: np.ndarray,
                                             macd_buy_sell_points: np.ndarray) -> np.ndarray:
    new_buy_sell_points = []
    index_x = 0
    for i in range(len(macd_buy_sell_points)):
        x = macd_buy_sell_points[i][0]
        for j in range(index_x + 1, len(x_axis)):
            if x_axis[j - 1] > x > x_axis[j]:
                index_x = j - 1
                break
        x = x_axis[index_x]
        y = y_axis[index_x]
        new_buy_sell_points.append((x, y))
    return new_buy_sell_points


def create_macd_plot(y1_axis: np.ndarray, y2_axis: np.ndarray, x_axis: np.ndarray, buy_sell_signals: np.ndarray,
                     macd_buy_sell_points: np.ndarray) -> str:
    line_width = 1

    plt.figure(figsize=(16, 9), dpi=100)

    plt.plot(x_axis, y1_axis, linestyle="-", color="blue", label="MACD", linewidth=line_width)
    plt.plot(x_axis, y2_axis, linestyle="-", color="red", label="SIGNAL", linewidth=line_width)

    plot_buy_sell_signals(buy_sell_signals, macd_buy_sell_points, False, False)

    plt.xlabel("Data")
    plt.ylabel("Wartość")
    plt.title("Wykres MACD/SIGNAL spółki PZU S.A. w okresie 04.01.2021 - 28.02.2025")
    plt.legend()
    plt.grid(True)
    # plt.show()

    filename = "macd_pzu.jpg"
    # plt.savefig(filename, dpi=800, bbox_inches="tight")
    print("Plot created")

    return filename


def plot_buy_sell_signals(buy_sell_signals, buy_sell_points, print_values=True, print_dates=True):
    marker_size = 80
    buy_label_added = False
    sell_label_added = False
    margin_buy_price = 0.5
    margin_buy_date = 1
    margin_sell_price = 0.5
    margin_sell_date = 1
    for index, (x_intersection, y_intersection) in enumerate(buy_sell_points):
        dt = x_intersection.strftime("%d.%m.%Y")
        if buy_sell_signals[index] == Signal.BUY:
            if not buy_label_added:
                plt.scatter(x_intersection, y_intersection, color='green', marker='^', s=marker_size,
                            label="Sygnał kupna")
                if print_values:
                    plt.text(x_intersection, y_intersection + margin_buy_price, str(round(y_intersection, 2)) + " zł",
                             fontsize=12, ha='center', color='green', fontweight='bold')
                if print_dates:
                    plt.text(x_intersection, y_intersection + margin_buy_date, dt, fontsize=12, ha='center',
                             color='green', fontweight='bold')
                buy_label_added = True
            else:
                plt.scatter(x_intersection, y_intersection, color='green', marker='^', s=marker_size)
                if print_values:
                    plt.text(x_intersection, y_intersection + margin_buy_price, str(round(y_intersection, 2)) + " zł",
                             fontsize=12, ha='center', color='green', fontweight='bold')
                if print_dates:
                    plt.text(x_intersection, y_intersection + margin_buy_date, dt, fontsize=12, ha='center',
                             color='black', fontweight='bold')
        else:
            if not sell_label_added:
                plt.scatter(x_intersection, round(y_intersection, 2), color='red', marker='v', s=marker_size,
                            label="Sygnał sprzedaży")
                if print_values:
                    plt.text(x_intersection, y_intersection - margin_sell_price, str(round(y_intersection, 2)) + " zł",
                             fontsize=12, ha='center', color='red', fontweight='bold')
                if print_dates:
                    plt.text(x_intersection, y_intersection - margin_sell_date, dt, fontsize=12, ha='center',
                             color='black', fontweight='bold')
                sell_label_added = True
            else:
                plt.scatter(x_intersection, y_intersection, color='red', marker='v', s=marker_size)
                if print_values:
                    plt.text(x_intersection, y_intersection - margin_sell_price, str(round(y_intersection, 2)) + " zł",
                             fontsize=12, ha='center', color='red', fontweight='bold')
                if print_dates:
                    plt.text(x_intersection, y_intersection - margin_sell_date, dt, fontsize=12, ha='center',
                             color='black', fontweight='bold')


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
                buy_sell_signals.append(Signal.BUY)
            if macd[i - 1] < signal[i - 1] and macd[i] > signal[i]:
                buy_sell_signals.append(Signal.SELL)
            cross_points.append((x_intersection, y_intersection))
    buy_sell_signals = np.array(buy_sell_signals)
    cross_points = np.array(cross_points)
    return buy_sell_signals, cross_points


def calculate_ema(data: np.ndarray, n: int) -> np.ndarray:
    alpha = 2 / (n + 1)
    ema = np.zeros_like(data)
    data_copy = data[::-1]
    ema[0] = data_copy[0]

    for i in range(1, len(data_copy)):
        ema[i] = alpha * data_copy[i] + (1 - alpha) * ema[i - 1]

    return ema[::-1]


def plot_investment_history(account_history: np.ndarray):
    # plt.ion()
    plt.figure(figsize=(16, 9), dpi=100)

    plt.bar(list(range(1, (len(account_history) + 1))), account_history, color="blue", label="Historia stanu portfela")
    plt.xlabel("Numer transakcji")
    plt.ylabel("Wartość całego kapitału [zł] (liczba akcji * cena akcji + wolna gotówka)")
    plt.title("Wykres wartości majatku inwestora")
    plt.legend()
    plt.grid(True)

    # colors = []
    # for t in transaction_results:
    #     if t == 1:
    #         colors.append('red')
    #     else:
    #         colors.append('green')
    #
    # plt.scatter([], [], color='green', label='Transakcja zyskowna')  # Pusta kropka dla legendy
    # plt.scatter([], [], color='red', label='Transakcja stratna')  # Pusta kropka dla legendy
    # plt.legend()
    #
    # plt.scatter(list(range(1, (len(transaction_results) + 1))), transaction_results, c=colors, s=100)
    # plt.xlabel("Numer transakcji")
    # plt.yticks([])
    # plt.title("Wykres historii rezultatów transakcji")

    print("Plot created")
    return


def simulation(buy_sell_signals: np.ndarray, buy_sell_points: np.ndarray) -> int:
    actions = 1000
    money = 0

    buy_sell_signals = buy_sell_signals[::-1]
    buy_sell_points = buy_sell_points[::-1]

    actions_history = [actions]
    money_history = [money]
    prices_history = [32.03]
    transaction_results = []
    profit_transactions_counter = 0
    loss_transactions_counter = 0

    account_history = [actions_history[0] * prices_history[0] + money_history[0]]

    iterations = len(buy_sell_signals)
    if buy_sell_signals[len(buy_sell_signals) - 1] == Signal.SELL:
        iterations = len(buy_sell_signals) - 1

    for i in range(iterations + 1):
        price = round(buy_sell_points[i], 2)
        prices_history.append(price)
        signal = buy_sell_signals[i]
        if signal == Signal.BUY:
            actions_to_buy = money // price
            money -= actions_to_buy * price
            actions += actions_to_buy
        else:
            actions_to_sell = int(actions*0.5)
            money += actions_to_sell * price
            actions -= actions_to_sell
        actions_history.append(actions)
        money_history.append(money)
        account_history.append(actions * price + money)
        # if buy_sell_signals[0] == Signal.BUY and i >= 1 and i % 2 == 1:
        if i >= 1 and i % 2 == 1:
            if account_history[i + 1] > account_history[i]:
                transaction_results.append(TransactionResult.PROFIT.value)
                profit_transactions_counter += 1
            else:
                transaction_results.append(TransactionResult.LOSS.value)
                loss_transactions_counter += 1
        # if buy_sell_signals[0] == Signal.SELL and i >= 2 and i % 2 == 0:
        #     if (actions_history[i - 1] * prices_history[i - 1] + money_history[i - 1]) < (
        #             actions_history[i] * prices_history[i] + money_history[i]):
        #         transaction_results.append(TransactionResult.PROFIT.value)
        #         profit_transactions_counter += 1
        #     else:
        #         transaction_results.append(TransactionResult.LOSS.value)
        #         loss_transactions_counter += 1
        if i == iterations - 1:
            print("-----------PRZED OSTATNIA SPRZEDAZA-----------")
            print("Stan portfela akcji: ", int(actions))
            print("Stan wolnej gotówki [zł]: ", money)
            print("----------------------------------------------")

    print("Stan portfela [zł]: ", money)
    print("Stan portfela akcji: ", int(actions))
    print("Wartosc akcji: ", int(actions) * 53.92)

    print()
    print()

    print("Transakcje zyskowne: ", int(profit_transactions_counter))
    print("Transakcje stratne: ", int(loss_transactions_counter))
    plot_investment_history(account_history)
    return actions


def main():
    # plt.ion()
    print("Program started")
    data = import_data("Historyczne ceny PZU.csv")
    ema12 = calculate_ema(data[:, 1], 12)
    ema26 = calculate_ema(data[:, 1], 26)
    macd = ema12 - ema26
    signal = calculate_ema(macd, 9)
    buy_sell_signals, cross_points = find_buy_sell_points(macd, signal, data[:, 0])

    create_macd_plot(macd, signal, data[:, 0], buy_sell_signals, cross_points)
    create_a_quote_plot(data[:, 0], data[:, 1], buy_sell_signals, cross_points)
    # plt.show()

    new_cross_points = np.array(find_new_axis_values_for_buy_sell_points(data[:, 0], data[:, 1], cross_points))[:, 1]
    simulation(buy_sell_signals, new_cross_points)


if __name__ == '__main__':
    main()
    print("Presss ENTER to exit")
    input()
