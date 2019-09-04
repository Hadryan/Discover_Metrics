import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# This function will display the exploratory data analysis for 

def exploratory_data_analysis():

    liked_dataset = pd.read_csv('liked_song_metrics.csv')
    disliked_dataset = pd.read_csv('disliked_song_metrics.csv')
    
    for i in range(1, 11):
        if i == 5:
            continue
        X = liked_dataset.iloc[1:,i].values.astype(float)
        X2 = disliked_dataset.iloc[1:,i].values.astype(float)
        index_liked = np.arange(len(X))
        index_disliked = np.arange(len(X2))
        plt.bar(index_liked, X)
        plt.bar(index_disliked, X2)
        plt.xlabel('song')
        plt.ylabel(liked_dataset.iloc[0:,i].values[0])
        plt.title(str(liked_dataset.iloc[0:,i].values[0]) + ' for Liked and Disliked Songs')
        plt.legend(["Liked", "Disliked"])
        plt.show()
