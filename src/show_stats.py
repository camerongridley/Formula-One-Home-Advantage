import numpy as np
import scipy.stats as stats

class ShowStats:

    def __init__(self):
        pass

    def print_basic_stats(self, one_d_array, data_label='data'):
        print(f'Mean of {data_label} {np.round(np.mean(one_d_array), 3)}')
        print(f'Variance of {data_label} {np.round(np.var(one_d_array), 3)}')
        print(f'Standard Deviation of {data_label} {np.round(np.mean(one_d_array), 3)}')

    def print_t_test_ind(self, a, b, data_label='data'):
        t_score, p = stats.ttest_ind(a,b)
        print(f't-test (ind) for {data_label}: p={np.round(p, 3)}, t_score={np.round(t_score, 3)}')
        return t_score, p