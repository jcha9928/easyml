"""
Functions for random forest analysis.
"""
import matplotlib.pyplot as plt
import numpy as np
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier

from .core import easy_analysis


__all__ = ['easy_random_forest']


class easy_random_forest(easy_analysis):
    def __init__(self, data, dependent_variable,
                 algorithm='random_forest', family='gaussian',
                 resample=None, preprocess=None, measure=None,
                 exclude_variables=None, categorical_variables=None,
                 train_size=0.667, survival_rate_cutoff=0.05,
                 n_samples=1000, n_divisions=1000, n_iterations=10,
                 random_state=None, progress_bar=True, n_core=1,
                 generate_coefficients=False,
                 generate_variable_importances=True,
                 generate_predictions=True, generate_model_performance=True,
                 model_args=None):
        super().__init__(data, dependent_variable,
                         algorithm=algorithm, family=family,
                         resample=resample, preprocess=preprocess, measure=measure,
                         exclude_variables=exclude_variables, categorical_variables=categorical_variables,
                         train_size=train_size, survival_rate_cutoff=survival_rate_cutoff,
                         n_samples=n_samples, n_divisions=n_divisions, n_iterations=n_iterations,
                         random_state=random_state, progress_bar=progress_bar, n_core=n_core,
                         generate_coefficients=generate_coefficients,
                         generate_variable_importances=generate_variable_importances,
                         generate_predictions=generate_predictions,
                         generate_model_performance=generate_model_performance,
                         model_args=model_args)

    def create_estimator(self):
        if self.family == 'gaussian':
            estimator = RandomForestRegressor()
        elif self.family == 'binomial':
            estimator = RandomForestClassifier()
        return estimator

    def extract_variable_importances(self, estimator):
        return estimator.feature_importances_

    def process_variable_importances(self, variable_importances):
        return variable_importances

    def predict_model(self, model, X):
        if self.family == 'gaussian':
            predictions = model.predict(X)
        elif self.family == 'binomial':
            predictions = model.predict_proba(X)
            predictions = predictions[:, 1]
        return predictions

    def plot_variable_importances(self):
        n = self.variable_importances.shape[1]
        importances_mean = np.mean(self.variable_importances, axis=0)
        column_names = [v[1] for v in sorted(zip(importances_mean, self.column_names), reverse=True)]
        importances_std = np.std(self.variable_importances, axis=0)
        importances_std = [v[1] for v in sorted(zip(importances_mean, importances_std), reverse=True)]
        importances_mean = sorted(importances_mean, reverse=True)

        fig, ax = plt.figure(), plt.gca()
        ax.bar(range(n), importances_mean, color='grey', ecolor='black',
               yerr=importances_std, align='center')
        ax.set_xticks(range(n))
        ax.set_xticklabels(column_names)
        ax.set_xlabel('Predictors')
        ax.set_ylabel('Variable Importance (Mean Decrease in Gini Index)')
        ax.set_title('Variable Importances')
        return fig
