import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main():
    df = pd.read_csv('data.csv')
    Rs = df.loc[:, 'Resistance']

    mean = np.mean(Rs)
    sigma = np.std(Rs)
    print(len(Rs))
    print(f'sigma: {len(list(filter(lambda R: abs(R - mean) < sigma, Rs)))}')
    print(f'2sigma: {len(list(filter(lambda R: abs(R - mean) < 2*sigma, Rs)))}')

    # plot(Rs, 10)
    # plot(Rs, 20)


def plot(Rs, m):
    export_split(Rs, m)

    fig, ax = plt.subplots()
    ax.set_title('Распределение сопротивлений')
    ax.set_xlabel('сопротивление (Ом)')
    ax.set_ylabel('вероятность')

    colors = ['#9f1853', '#fa4d56', '#570408', '#a56eff']
    n, bins, _ = ax.hist(
        Rs,
        bins=m,
        density=True,
        color=colors[0],
        edgecolor='white',
        label='W(Rᵢ)'
    )
    sup = max(n)
    mean = np.mean(Rs)
    sigma = np.std(Rs)
    ax.vlines(
        mean,
        0,
        sup,
        color=colors[1],
        linestyles='dashdot',
        label='⟨R⟩',
    )
    ax.vlines(
        [mean - sigma, mean + sigma],
        0,
        sup,
        color=colors[2],
        linestyles='dashed',
        label='⟨R⟩±σ',
    )
    x = np.arange(Rs.min(), Rs.max(), 0.1)
    ax.plot(
        x,
        1 / (np.sqrt(2 * np.pi) * sigma) *
        np.exp(-(x - mean) ** 2 / (2 * sigma ** 2)),
        color=colors[3],
    )

    ax.legend()
    fig.savefig(f'distrib_{m}bins.png')


def export_split(Rs, m):
    n, bins, _ = plt.hist(Rs, m)
    df = pd.DataFrame({
        'bins': [(bins[i] + bins[i + 1]) / 2 for i in range(m)],
        'n': n,
        'W': np.round(n/len(Rs) * 100, 1),
    })
    df.to_csv(f'probs_{m}bins.csv')

main()
