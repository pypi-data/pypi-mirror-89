import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


data = np.array([
    [0.58576, 0.59834, 0.5988, 0.61278, 0.62092],
    [0.59112, 0.6047, 0.61794, 0.62962, 0.62688],
    [0.59982, 0.61644, 0.62758, 0.63568, 0.63638],
    [0.60112, 0.61944, 0.626, 0.63798, 0.64436],
    [0.61334, 0.60912, 0.63342, 0.63894, 0.64726]
])

tick = [32, 40, 48, 56, 64]
data=pd.DataFrame(data, index=tick, columns=tick)
sns.heatmap(data, annot=True)
plt.show()
