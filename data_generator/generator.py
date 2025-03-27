from Minesweeper_Gen_Partial import Minesweeper_Partial
from processing import extract_feature
from tqdm import tqdm
import pandas as pd
import numpy as np

path_data = '../dataset/data.csv'
path_label = '../dataset/label.csv'

def generate_data(number_of_board):
    data = []
    labels = []
    progress = tqdm(total=number_of_board)
    current_board = 0
    while current_board < number_of_board:
        game = Minesweeper_Partial()
        partial_board = game.transform_partial()
        features = extract_feature(partial_board)
        label = game.get_label()
        num_ratio, hidden_ratio, flag_ratio, = game.cell_ratio(partial_board)
        if num_ratio > 0.5 and num_ratio < 0.6 and hidden_ratio > 0.3 and hidden_ratio < 0.4 and flag_ratio > 0.05 and flag_ratio < 0.12:
            data.append(features)
            labels.append(label)
            current_board += 1
            progress.update(1)
    progress.close()
    return np.array(data).reshape(-1, 27), np.array(labels).reshape(-1, 1)

def save_to_csv(data, path_data, label, path_label):
    feature = pd.DataFrame(data)
    feature.to_csv(path_data, header=None, index=False)
    label = pd.DataFrame(label)
    label.to_csv(path_label, header=None, index=False)

data, label = generate_data(10_000)
print(data.shape, label.shape)
save_to_csv(data, path_data, label, path_label)
print("Done")