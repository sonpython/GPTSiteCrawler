import matplotlib.pyplot as plt
import pandas as pd
import time


def plot_crawl_stats(filename):
    plt.ion()
    fig, ax = plt.subplots()

    while True:
        df = pd.read_csv(filename)
        ax.clear()

        ax.plot(df['Time'], df['Links in Queue'], label='Links in Queue')
        ax.plot(df['Time'], df['Visited Links'], label='Visited Links')
        # ax.set_xlabel('Time')
        plt.xticks([])
        ax.set_ylabel('Number of Links')
        ax.set_title('Crawler Statistics Over Time')
        ax.legend()
        plt.xticks(rotation=45)
        plt.tight_layout()

        plt.pause(1)
        plt.draw()


if __name__ == "__main__":
    plot_crawl_stats('crawl_stats.csv')
