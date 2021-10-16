import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

num_schemes = 5
num_lengthes = 4


def main():

    I, U, l = parse_schemes()

    def plot_l_lines(ax):
        colors = ['#6929c4', '#012749', '#009d9a', '#ee538b']
        for i in range(num_lengthes):
            k, b = np.polyfit(U[i], I[i], 1)
            x = np.arange(max(U[i]) + 0.2, step=0.1)
            ax.plot(x, k * x + b, color=colors[i],
                    label=f'l = {round(l[i])} см')
            ax.scatter(U[i], I[i], c=colors[i] + '40', edgecolors=colors[i])
        ax.legend()

    def plot_s_lines(ax):
        for j in range(num_schemes):
            k, b = np.polyfit(U[:, j], I[:, j], 1)
            x = np.arange(U[:, j].min() - 0.2, U.max() + 0.2, step=0.1)
            ax.plot(x, k * x + b, color='#a8a8a8', ls='--')

    fig, ax = new_plot()
    plot_l_lines(ax)
    fig.savefig('ivc.png')

    fig, ax = new_plot()
    plot_s_lines(ax)
    plot_l_lines(ax)
    fig.savefig('ivc+.png')

    Rs = [U[i] / I[i] for i in range(num_lengthes)]

    fig, ax = plt.subplots()
    ax.set_title('Сравнение методов измерения')


def new_plot():
    fig, ax = plt.subplots()
    ax.set_title('Вольт-Амперная Характеристика')
    ax.set_ylabel('Сила тока через источник (А)')
    ax.set_xlabel('Напряжение на проволоке (В)')
    ax.grid()
    return fig, ax


def read_from_scheme(i):
    df = pd.read_csv(f'schemes/{i + 1}.csv')
    return df


def parse_schemes():
    I = np.empty((num_lengthes, num_schemes))
    U = np.empty((num_lengthes, num_schemes))
    l = np.empty(num_lengthes)
    for j in range(num_schemes):
        df = read_from_scheme(j)
        I[:, j] = df.loc[:, 'I']
        U[:, j] = df.loc[:, 'U']
        l[:] = df.loc[:, 'l']
    return I, U, l


main()
