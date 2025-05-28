import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas as pd
from scipy.optimize import minimize


def opt_acc(n_correct, y_test, n_pos, wc):

	weight = np.array([1.0] * y_test.shape[0])
	new_weight = weight * (wc * (y_test + 1.0) * 0.5 - (y_test - 1.0) * 0.5)
	weight_dist = np.linalg.norm(new_weight - weight)
	print(f'{weight_dist=}')

	binary = np.array([1.] * n_correct + [0.] * (len(y_test) - n_correct))

	w0 = np.ones_like(binary) / len(binary)  # wの初期値
	w_tilde = np.array([1.0] * len(binary))

	def objective(w):
		return np.dot(binary, w) / np.sum(w)
	def constraint_sum(w):
		return np.sum(w) - np.sum(w_tilde)
	def constraint_sphere(w):
		return weight_dist - np.linalg.norm(w - w_tilde)

	cons = [{'type': 'eq', 'fun': constraint_sum},
			{'type': 'ineq', 'fun': constraint_sphere}]
	bounds = [(0, None) for _ in range(len(w0))] # w >= 0という制約

	res = minimize(objective, w0, method='SLSQP', bounds=bounds, constraints=cons)
	acc_w = res.fun
	w_te = res.x

	return acc_w, w_te

wc = float(sys.argv[1])
method = sys.argv[2]

fname = f'/home/tanaka.tomonari/DeepCore-main/result/{method}_0.csv'
df = pd.read_csv(fname)
fraction_list = df['Fraction'].tolist()

# calculate acc_weight
acc_w_list = []
for iter in range(len(fraction_list)):
	n_pos = df['N_pos'].tolist()[iter]
	n_correct = df['Correct'].tolist()[iter]
	n_total = df['Total'].tolist()[iter]
	y_test = np.array([1.] * n_pos + [-1.] * (n_total - n_pos))
	print(f'wc={wc}, method:{method}, iter={iter}')
	if wc == 1.0:
		acc_w = n_correct / n_total
	else:
		acc_w, _ = opt_acc(n_correct, y_test, n_pos, wc)
	acc_w_list.append(acc_w)

df["Acc"] = acc_w_list

print('==================')

output_file_path = f"/home/tanaka.tomonari/DeepCore-main/result/{method}_weight_{wc}.csv"
df.to_csv(output_file_path, index=False)
