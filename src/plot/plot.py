import pandas as pd
import matplotlib.pyplot as plt


def draw_plot():
    """
    Crée et enregistre deux graphiques à barres:
    1. Un graphique montrant le nombre de poèmes/dynastie
    2. Un graphique montrant la longueur moyenne des poèmes/dynastie

    Returns:
        None
    """
    dynasties = ['WeiJin', 'NanBei', 'Tang', 'Song', 'Yuan', 'Ming', 'Qing']
    data_frames = []
    for dyansty in dynasties:
        df = pd.read_csv(f'./data/raw/temp_{dyansty}_poems.csv')
        data_frames.append(df)

    poem_counts = [len(df) for df in data_frames]
    avg_lens = [df['Content'].apply(len).mean() for df in data_frames]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    ax1.bar(dynasties, poem_counts)
    ax1.set_title('poems for each dynasty')

    ax2.bar(dynasties, avg_lens)
    ax2.set_title('average length of poems for each dynasty')

    plt.savefig('./figures/dynasty_poems_stats.png',
                dpi=300, bbox_inches='tight')


def main():
    draw_plot()


if __name__ == '__main__':
    main()
