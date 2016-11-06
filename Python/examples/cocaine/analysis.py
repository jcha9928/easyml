from glmnet import LogitNet
import matplotlib as mpl
import numpy as np

# Set matplotlib settings
mpl.get_backend()
mpl.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from easyml.bootstrap import bootstrap_aucs, bootstrap_coefficients, bootstrap_predictions
from easyml.datasets import cocaine
from easyml.plot import plot_auc_histogram, plot_roc_curve
from easyml.utils import process_coefficients, process_data
from easyml.sample import sample_equal_proportion


# Analysis constants
EXCLUDE_AGE = False
TRAIN_SIZE = 0.667
N_DIVISIONS = 1000
N_ITERATIONS = 10
N_SAMPLES = 1000

# Model constants
ALPHA = 1
CUT_POINT = 0  # use 0 for minimum, 1 for within 1 SE
MAX_ITER = 1e6
N_FOLDS = 5
N_LAMBDA = 200
STANDARDIZE = False

# Create model
lr = LogitNet(alpha=ALPHA, cut_point=CUT_POINT, max_iter=MAX_ITER, n_folds=N_FOLDS, n_lambda=N_LAMBDA, standardize=STANDARDIZE)

# Load data
data = cocaine.load_data()

# Exclude certain variables
variables = ['subject']

if EXCLUDE_AGE:
    variables.append('AGE')

# Process the data
X, y = process_data(data, dependent_variables='DIAGNOSIS', exclude_variables=variables)

##############################################################################
# Replicating figure 1 - Done!
##############################################################################
# Bootstrap coefficients
coefs = bootstrap_coefficients(lr, X, y)

# Process coefficients
betas = process_coefficients(coefs)
betas.to_csv('./results/betas.csv', index=False)

##############################################################################
# Replicating figure 2 - Done!
##############################################################################
# Split data
mask = sample_equal_proportion(y, proportion=TRAIN_SIZE, random_state=43210)
y_train = y[mask]
y_test = y[np.logical_not(mask)]
X_train = X[mask, :]
X_test = X[np.logical_not(mask), :]

# Bootstrap predictions
all_y_train_scores, all_y_test_scores = bootstrap_predictions(lr, X_train, y_train, X_test, y_test, n_samples=N_SAMPLES)

# Generate scores for training and test sets
y_train_scores_mean = np.mean(all_y_train_scores, axis=0)
y_test_scores_mean = np.mean(all_y_test_scores, axis=0)

# Compute ROC curve and ROC area for training
plot_roc_curve(y_train, y_train_scores_mean)
plt.savefig('./results/train_roc_curve.png')

# Compute ROC curve and ROC area for test
plot_roc_curve(y_test, y_test_scores_mean)
plt.savefig('./results/test_roc_curve.png')

##############################################################################
# Replicating figure 4 - Done!
##############################################################################
all_train_aucs, all_test_aucs = bootstrap_aucs(lr, X, y, n_divisions=N_DIVISIONS, n_iterations=N_ITERATIONS)

# Plot histogram of training AUCS
plot_auc_histogram(all_train_aucs)
plt.savefig('./results/train_auc_distribution.png')

# Plot histogram of test AUCS
plot_auc_histogram(all_test_aucs)
plt.savefig('./results/test_auc_distribution.png')
