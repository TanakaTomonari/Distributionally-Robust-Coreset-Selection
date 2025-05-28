import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas as pd

# method_list = []
method_list = ['Proposed', 'DeepFool', 'Forgetting', 'Glister', 'GraNd', 'Submodular', 'Uncertainty']
# method_list = ['DeepFool', 'Forgetting', 'Glister', 'GraNd', 'Submodular', 'Uncertainty']
n_full = 40000
lam = '40'

# fraction_listを取得
fname = os.path.join('baselines', f'DeepFool_weight_1.0.csv')
df = pd.read_csv(fname)
fraction_list = df['Fraction'].tolist()

# for wc in [1.01, 1.03, 1.05, 1.07]:
# for wc in [1.01]:
for wc in np.arange(1.01, 1.05, 0.01):
	print(f'a={wc}')

	plt.figure(figsize=(9,7))
	plt.subplots_adjust(top=0.95, bottom=0.2)
	savename = f'cifar10_{wc}.pdf'
	# plt.figure(figsize=)

	for method in method_list:

		acc_list = []
		if method == 'Proposed':
			# acc
			datafile = os.path.join('proposed', f'acc_{n_full}_{n_full}_{wc:.5f}_heuristicsonce.csv')
			data = pd.read_csv(datafile, header=None)
			acc_list = data.iloc[0].tolist()
			print(fraction_list)
			print(acc_list)
			plt.plot(1-np.array(fraction_list)[::-1], acc_list, c='r', lw=3.0, label=method)

		else:
			fname = os.path.join('baselines', f'{method}_weight_{wc}.csv')
			df = pd.read_csv(fname)
			fraction_list = df['Fraction'].tolist()
			acc_list = df['Acc'].tolist()

			print('==================')
			print(len(acc_list))

			# make a figure
			print(fraction_list)
			plt.plot(1-np.array(fraction_list), acc_list, lw=2.0, label=method)

	plt.grid(True, alpha=0.2)
	# plt.xlim((0.0, 1.0))
	plt.ylim((0.3, 1.0))
	plt.xlabel('Sample deletion ratio [-]')
	# plt.title(r'$a=$' + f'{weight}, {data}')
	# plt.ylabel(r'$E_{test}$')
	plt.ylabel('Accuracy [-]')
	plt.rcParams["font.size"] = 18
	plt.legend()
	# plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
	plt.savefig(savename, bbox_inches='tight')
	plt.close()