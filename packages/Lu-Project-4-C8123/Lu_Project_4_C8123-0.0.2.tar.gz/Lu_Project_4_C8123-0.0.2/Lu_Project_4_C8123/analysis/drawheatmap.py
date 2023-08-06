import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


def sample_net_search_figure():
    """
        draw the heatmap for search result
    """
    data = np.array([
        [0.57876, 0.58238, 0.59244, 0.59662, 0.60702],
        [0.58844, 0.60174, 0.60968, 0.60948, 0.60714],
        [0.59464, 0.6086, 0.6222, 0.6165, 0.62658],
        [0.60702, 0.62248, 0.63056, 0.63378, 0.63042],
        [0.61884, 0.61976, 0.63092, 0.63564, 0.63704],
    ])
    tick = [32, 40, 48, 56, 64]
    data = pd.DataFrame(data, index=tick, columns=tick)
    sns.heatmap(data, annot=True)
    plt.xlabel("2nd CNN Layer Channel")
    plt.ylabel("1st CNN Layer Channel")
    plt.show()
