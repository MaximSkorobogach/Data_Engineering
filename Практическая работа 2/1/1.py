import numpy as np
import json

matrix = np.load('matrix_49.npy')

total_sum = np.sum(matrix)
total_avg = np.mean(matrix)

main_diag = np.diagonal(matrix)
sum_main_diag = np.sum(main_diag)
avg_main_diag = np.mean(main_diag)

side_diag = np.diagonal(np.flipud(matrix))
sum_side_diag = np.sum(side_diag)
avg_side_diag = np.mean(side_diag)

max_value = np.max(matrix)
min_value = np.min(matrix)

result = {
    "sum": int(total_sum),
    "avr": float(total_avg),
    "sumMD": int(sum_main_diag),
    "avrMD": float(avg_main_diag),
    "sumSD": int(sum_side_diag),
    "avrSD": float(avg_side_diag),
    "max": int(max_value),
    "min": int(min_value)
}

with open('result.json', 'w') as json_file:
    json.dump(result, json_file)

normalized_matrix = (matrix - min_value) / (max_value - min_value)
np.save('normalized_matrix.npy', normalized_matrix)