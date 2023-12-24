import numpy as np

matrix = np.load('matrix_49_2.npy')

x = np.array([])
y = np.array([])
z = np.array([])

# 500 + вариант, вариант 49
threshold = 500 + 49

for i in range(matrix.shape[0]):
    for j in range(matrix.shape[1]):
        if matrix[i, j] > threshold:
            x = np.append(x, i)
            y = np.append(y, j)
            z = np.append(z, matrix[i, j])

np.savez('result.npz', indices=x, values=y, other_values=z)
np.savez_compressed('result_compressed.npz', indices=x, values=y, other_values=z)

import os
print(f"Размер 'result.npz': {os.path.getsize('result.npz')} байт")
print(f"Размер 'result_compressed.npz': {os.path.getsize('result_compressed.npz')} байт")