import numpy as np
from math import log


class LinearRegression:
    def __init__(self):
        self.b0 = -1
        self.b1 = -1
        self.x_train = None
        self.y_train = []
        self.x_test = None
        self.y_test = []
        self.y_pred = []

    @staticmethod
    def mean(arr):
        total = 0
        for i in arr:
            total += i
        return total / len(arr)

    def variance(self, arr):
        mean_arr = self.mean(arr)
        var = 0
        for i in arr:
            var += (i - mean_arr) ** 2
        return var

    def covariance(self, arr1, arr2):
        mean_arr1 = self.mean(arr1)
        mean_arr2 = self.mean(arr2)
        cov = 0
        for i in range(len(arr1)):
            cov += ((arr1[i] - mean_arr1) * (arr2[i] - mean_arr2))
        return cov

    def coefficients(self, x_train, y_train):
        # Y = MX + C
        self.b1 = self.covariance(x_train, y_train) / self.variance(x_train)
        self.b0 = self.mean(y_train) - self.b1 * self.mean(x_train)
        return self.b0, self.b1

    def fit(self, x_train, y_train):
        self.x_train, self.y_train = x_train, y_train
        self.b0, self.b1 = self.coefficients(x_train, y_train)
        return self

    def predict(self, x_test):
        self.x_test = x_test
        predictions = []
        for i in x_test:
            predictions.append(self.b0 + self.b1 * i)
        return predictions

    def rmse_metric(self):
        mse = np.sum((self.y_pred - self.y_test) ** 2)
        return np.sqrt(mse / len(self.y_test))

    def r_square_metric(self):
        ssr = np.sum((self.y_pred - self.y_test) ** 2)
        sst = np.sum((self.y_test - np.mean(self.y_test)) ** 2)
        r2_score = 1 - (ssr / sst)
        return r2_score

    def adj_r_square_metric(self):
        r2_score = self.r_square_metric()
        n, k = self.x_test.shape[0], self.x_test.shape[1]
        aj_r2 = 1 - ((1 - r2_score) * (n - 1) / (n - k - 1))
        return aj_r2

    def standard_error_metric(self):
        sse = np.sum((self.predict(self.x_test) - self.y_test) ** 2, axis=0) / \
              float(self.x_test.shape[0] - self.x_test.shape[1])
        se = np.array([np.sqrt(np.diagonal(sse * np.linalg.inv(np.dot(self.x_test.T, self.x_test))))])[0][0]
        return se

    def f_stat_metric(self):
        sse = np.sum((self.y_pred - self.y_test) ** 2)
        rss = np.sum((self.y_pred - self.mean(self.y_test)) ** 2)
        n, k = self.x_test.shape[0], self.x_test.shape[1]
        msr = rss / n
        f_test = msr / (sse / n - (k + 1))
        return f_test

    def likelihood_metric(self):
        mse = np.sum((self.y_pred - self.y_test) ** 2)
        return log(mse)

    def aic_metric(self):
        num_params = 2
        mse = np.sum((self.y_pred - self.y_test) ** 2)
        aic = self.x_test.shape[0] * log(mse) + 2 * num_params
        return aic

    def bic_metric(self):
        num_params = 2
        mse = np.sum((self.y_pred - self.y_test) ** 2)
        bic = self.x_test.shape[0] * log(mse) + num_params * log(self.x_test.shape[0])
        return bic

    def summary(self, y_test, y_pred):
        self.y_test = y_test
        self.y_pred = y_pred
        print('RMSE: ', self.rmse_metric())
        print('R-square: ', self.r_square_metric())
        print('Adj. R-squared: ', self.adj_r_square_metric())
        print('standard_error: ', self.standard_error_metric())
        print('F-statistic ', self.f_stat_metric())
        print('Log-Likelihood: ', self.likelihood_metric())
        print('AIC: ', self.aic_metric())
        print('BIC: ', self.bic_metric())
