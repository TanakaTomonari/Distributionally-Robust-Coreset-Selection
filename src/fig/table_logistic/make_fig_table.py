import matplotlib.pyplot as plt
import numpy as np
import csv
import sys
import os
import pandas as pd


def numform(value, digits):
    s = str(value)
    pos = s.find('.')
    if pos == -1:
        if len(s) <= digits - 2:
            return s + '.0'
        else:
            return s
    else:
        if pos >= digits - 1:
            return s[:pos]
        else:
            return s[:(digits+1)]



mode = sys.argv[1]	# kernel or linear or cntk
data = sys.argv[2] # dataset
dir_data = os.path.join(f'{data}-logistic', f'{mode}')
tolerance = 0.0001

method_list = ['Proposed', 'Herding', 'Kcenter', 'Margin', 'Random']
# method_list = ['Proposed', 'Random']
num_dict = {'breast-cancer': 546, 'australian': 552, 'heart': 216, 'ionosphere_scale': 280, 'sonar_scale': 166, 'splice_scale': 800, 'cifar10': 1000}
lam_dict = {'breast-cancer': ['0.9', '0.546', '17.26', '546'], 'australian': ['0.552', '1.5', '17.45', '552'], 'heart': ['0.216', '2.7', '6.830', '216'], 'ionosphere_scale': ['0.03', '0.28', '8.854', '280'], 'sonar_scale': ['0.03', '0.166', '5.249', '166'], 'splice_scale': ['0.03', '0.8', '25.29', '800'], 'cifar10': ['0.01', '1.', '31.62', '1000']}
n_full = num_dict[data]
step = 2  # プロットの間隔を指定

for lam in lam_dict[data]:
# for lam in ((10.0 ** np.linspace(-3, 0, 7)) * (n_full)):
# for lam in [0.28, 0.885, 2.8, 8.854, 28.0, 88.54, 280]:

	# lam = numform(lam, 4)
	# lam = numform(lam, 4).rstrip('0')

	# Safe screening samples

	# for weight in np.arange(0.90, 1.10, 0.0025):
	# for weight in [1.01]:
	for weight in np.arange(1.00, 1.05, 0.01):
		fname = os.path.join(dir_data, f'lam_{lam}', f'a{weight:.5f}.pdf')

		# make figure
		# plt.figure(figsize=(8, 6))
		plt.figure(figsize=(9, 7))
		plt.subplots_adjust(top=0.95, bottom=0.2)

		# もしelseが複数回回る場合を考慮
		used_colors = []
		else_counter = 0

		for method in method_list:
			acc_list = []

			if method == 'Proposed':
				# datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_{weight:.5f}_heuristics.csv')
				datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_{weight:.5f}_greedy.csv')
				with open(datafile) as csvfile:
					reader = csv.reader(csvfile)
					for i, line in enumerate(list(reader)):
						acc = np.array((line),dtype=float)
						n_uss = len(np.array((line),dtype=float))

						# adjust number
						if n_uss > n_full:
							n_uss = n_full
							acc = acc[1::]

						# calcuration of number of samples
						n_ss = n_full - n_uss
						print(f'{n_uss=}')
						print(f'{n_ss=}')
						# make acc array of full lb
						acc_full = np.hstack((acc[0] * np.ones(n_ss), acc))
						acc_list.append(acc_full)
				ave_acc = np.mean(acc_list, axis=0)
				std_dev = np.std(acc_list, axis=0)

				plt.plot(np.arange(n_full)[::step]/n_full, ave_acc[::step], lw=2.0, c='r', label=method)
				plt.fill_between(np.arange(n_full)[::step]/n_full, ave_acc[::step] - std_dev[::step], ave_acc[::step] + std_dev[::step], color='r', alpha=0.2)  # Error band

			elif method == 'Random':
				datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_{weight:.5f}_{method}.csv')
				with open(datafile) as csvfile:
					reader = csv.reader(csvfile)
					for i, line in enumerate(list(reader)):
						acc = np.array((line),dtype=float)
						n_uss = len(np.array((line),dtype=float))

						# adjust number
						if n_uss > n_full:
							n_uss = n_full
							acc = acc[1::]

						# calcuration of number of samples
						n_ss = n_full - n_uss
						print(f'{n_uss=}')
						print(f'{n_ss=}')
						# make acc array of full lb
						acc_full = np.hstack((acc[0] * np.ones(n_ss), acc))
						acc_list.append(acc_full)
				ave_acc = np.mean(acc_list, axis=0)
				std_dev = np.std(acc_list, axis=0)

				plt.plot(np.arange(n_full)[::step]/n_full, ave_acc[::step], c='m', label=method)
				plt.fill_between(np.arange(n_full)[::step]/n_full, ave_acc[::step] - std_dev[::step], ave_acc[::step] + std_dev[::step], color='m', alpha=0.2)  # Error band

			else:
				# method_name = str.lower(method)
				datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_{weight:.5f}_{method}.csv')
				with open(datafile) as csvfile:
					reader = csv.reader(csvfile)
					for i, line in enumerate(list(reader)):
						acc = np.array((line),dtype=float)
						n_uss = len(np.array((line),dtype=float))

						# adjust number
						if n_uss > n_full:
							n_uss = n_full
							acc = acc[1::]

						# calcuration of number of samples
						n_ss = n_full - n_uss
						print(f'{n_uss=}')
						print(f'{n_ss=}')
						# make acc array of full lb
						acc_full = np.hstack((acc[0] * np.ones(n_ss), acc))
						acc_list.append(acc_full)
				tmp_ave_acc = np.mean(acc_list, axis=0)
				ave_acc = tmp_ave_acc[::-1]

				# 使用済みの色リストから次の色を選ぶ
				if else_counter == 0:
					# 最初は自動で選択された色を使用
					line1, = plt.plot(np.arange(n_full)[::step]/n_full, ave_acc[::step], label=method)
					color = line1.get_color()  # 最初のプロットの色を取得
					plt.fill_between(np.arange(n_full)[::step]/n_full, ave_acc[::step] - std_dev[::step], ave_acc[::step] + std_dev[::step], color=color, alpha=0.2)  # Error band
					used_colors.append(color)
				else:
					# 2回目以降は色を使い回さない
					color = plt.get_cmap('tab10')(else_counter % 10)  # `tab10`カラーマップで色を選ぶ
					while color in used_colors:
						else_counter += 1
						color = plt.get_cmap('tab10')(else_counter % 10)
					line1, = plt.plot(np.arange(n_full)[::step]/n_full, ave_acc[::step], label=method, color=color)
					used_colors.append(color)
					plt.fill_between(np.arange(n_full)[::step]/n_full, ave_acc[::step] - std_dev[::step], ave_acc[::step] + std_dev[::step], color=color, alpha=0.2)  # Error band
				else_counter += 1


		# guarantee data
		gua_list = []
		# datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_bound_heuristics_{weight:.5f}.csv')
		datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_bound_greedy_{weight:.5f}.csv')
		print(f'lam={lam}, weight={weight}')
		with open(datafile) as csvfile:
			reader = csv.reader(csvfile)
			for i, line in enumerate(list(reader)):
				if i % 2 == 0:
					lb = np.array((line),dtype=float)
					n_uss = len(np.array((line),dtype=float))

					# adjust number
					if n_uss > n_full:
						n_uss = n_full
						lb = lb[1::]

					# calcuration of number of samples
					n_ss = n_full - n_uss
					print(f'{n_uss=}')
					print(f'{n_ss=}')

					# make guarantee array of full lb
					gua = np.hstack((lb[0] * np.ones(n_ss), lb))
					print(len(gua))
					gua_list.append(gua)

		ave_gua = np.mean(gua_list, axis=0)
		std_dev = np.std(gua_list, axis=0)
		print(len(ave_gua))

		plt.plot(np.arange(n_full)[::step]/n_full, ave_gua[::step], ls=':', lw=2.0, c='b', label='Guarantee')
		plt.fill_between(np.arange(n_full)[::step]/n_full, ave_gua[::step] - std_dev[::step], ave_gua[::step] + std_dev[::step], color='b', alpha=0.2)  # Error band

		plt.grid(True, alpha=0.2)
		# plt.xlim((0, 1))
		plt.ylim((0.0, 1.0))
		plt.xlabel('Sample deletion ratio [-]')
		# plt.xscale("log")
		plt.title(r'$a=$' + f'{weight}, {data}')
		# plt.ylabel(r'$E_{test}$')
		plt.ylabel('Accuracy [-]')
		plt.rcParams["font.size"] = 18
		plt.legend()
		# plt.legend(loc='upper left', bbox_to_anchor=(1, 1))
		plt.savefig(fname, bbox_inches='tight')
		plt.close()



# ==========================================
step = 1
# dir_data = os.path.join(data, f'{mode}')
# tolerance = 0.0001

# for lam in [2000]:
for lam in lam_dict[data]:

	# make figure
	plt.figure(figsize=(9, 7))
	# plt.figure(figsize=(9, 3))
	plt.subplots_adjust(top=0.95, bottom=0.2)
	fname = f'{dir_data}/{mode}_ss_screening_rate_lam{lam}_x_n_y_etest.pdf'

	# for weight in np.arange(0.90, 1.10, 0.0025):
	# for weight in np.arange(1.04, 1.05, 0.01):
	for weight in np.arange(1.00, 1.05, 0.01):

		# guarantee data
		gua_list = []
		# datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_bound_heuristics_{weight:.5f}.csv')
		datafile = os.path.join(dir_data, f'lam_{lam}', f'sum_acc_bound_greedy_{weight:.5f}.csv')
		print(f'lam={lam}, weight={weight}')
		with open(datafile) as csvfile:
			reader = csv.reader(csvfile)
			for i, line in enumerate(list(reader)):
				if i % 2 == 0:
					lb = np.array((line),dtype=float)
					# print(lb[:10])
					n_uss = len(np.array((line),dtype=float))

					# adjust number
					if n_uss > n_full:
						n_uss = n_full
						lb = lb[1::]

					# calcuration of number of samples
					n_ss = n_full - n_uss
					print(f'{n_uss=}')
					print(f'{n_ss=}')

					# make guarantee array of full lb
					gua = np.hstack((lb[0] * np.ones(n_ss), lb))
					# print(len(gua))
					gua_list.append(gua)

		# print(gua_list[:-10])
		ave_gua = np.mean(gua_list, axis=0)
		# print(ave_gua[:-10])
		std_dev = np.std(gua_list, axis=0)
		# print(len(ave_gua))
		# sys.exit()

		plt.plot(np.arange(n_full)[::step]/n_full, ave_gua[::step], lw=2.0, label=r'$a=$'+ f'{weight}')
		# plt.fill_between(np.arange(n_full)[::step]/n_full, ave_gua[::step] - std_dev[::step], ave_gua[::step] + std_dev[::step], alpha=0.2)  # Error band

	if data == 'splice_scale':
		dataname = 'splice'
	else:
		dataname = data
	plt.title(f'{dataname}, ' + r'$\lambda=$' + f'{lam}')
	plt.grid(True, alpha=0.2)
	plt.xlim((0, 1))
	plt.ylim((0.0, 1.0))
	plt.xlabel('Sample deletion ratio [-]')
	# plt.ylabel(r'$E_{test}$')
	plt.ylabel('Accuracy [-]')
	plt.legend()
	plt.savefig(fname, bbox_inches='tight')
	plt.close()