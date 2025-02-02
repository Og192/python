import torch
import csv
import numpy as np

wine_path = "../../../../dlwpt-code/data/p1ch4/tabular-wine/winequality-white.csv"
wineq_numpy = np.loadtxt(wine_path, dtype=np.float32, delimiter=';', skiprows=1)
print(wineq_numpy)

col_list = next(csv.reader(open(wine_path), delimiter=';'))
print(wineq_numpy.shape, col_list)

wineq = torch.from_numpy(wineq_numpy)
print(wineq.shape, wineq.dtype)

data = wineq[:, :-1]
print(data, data.shape)

target = wineq[:, -1]
print(target, target.shape)

target = target.long()
print(target.long())

target_onehot = torch.zeros(target.shape[0], 10)
target_onehot.scatter_(1, target.unsqueeze(1), 1.0)

print(target_onehot)

target_unsequeezed = target.unsqueeze(1)
print(target_unsequeezed)

data_mean = torch.mean(data, dim=0)
print(data_mean)

data_var = torch.var(data, dim=0)
print(data_var)

data_normalized = (data - data_mean) / torch.sqrt(data_var)
print(data_normalized)

bad_indexes = target <= 3
print(bad_indexes.shape, bad_indexes.dtype, bad_indexes.sum())

# advanced indexing
bad_data = data[bad_indexes]
print(bad_data.shape)

# group
bad_data = data[target <= 3]
mid_data = data[(target > 3) & (target < 7)]
good_data = data[target >= 7]

bad_mean = torch.mean(bad_data, dim=0)
mid_mean = torch.mean(mid_data, dim=0)
good_mean = torch.mean(good_data, dim=0)

for i, args in enumerate(zip(col_list, bad_mean, mid_mean, good_mean)):
    print('{:2} {:20} {:6.2f} {:6.2f} {:6.2f}'.format(i, *args))

# threshold
total_sulfur_threshold = 141.83
total_sulfur_data = data[:, 6]
predicted_indexes = torch.lt(total_sulfur_data, total_sulfur_threshold)
print(predicted_indexes.shape, predicted_indexes.dtype, predicted_indexes.sum())

actual_indexes = target > 5
print(actual_indexes.shape, actual_indexes.dtype, actual_indexes.sum())

# see how well we did
# item() Returns the value of this tensor as a standard Python number. This only works for tensors with one element.
n_matches = torch.sum(actual_indexes & predicted_indexes).item()
n_predicted = torch.sum(predicted_indexes).item()
n_actual = torch.sum(actual_indexes).item()
print(n_matches, n_matches / n_predicted, n_matches / n_actual)

