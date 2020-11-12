# coding: utf-8
# Import packages
import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from src.linear_regression import get_polynomial_basis, get_sol, get_predictions 
from src.linear_regression import get_mse, get_ln_mse, run_polynomial_regression


def get_sin_basis(x): 
    '''
    ---------------------
    Input:
    Output: 
    ---------------------
    '''
    y_true = np.power(np.sin(2*math.pi*x),2)
    return y_true


def get_sin_features(x, k):
    


def run_sinusoid_regression(x, k):
    pass


def add_noise(y_true, loc = 0, sd = 0.07):
    '''
    ---------------------
    Input:
    Output: 
    ---------------------
    '''
    y_obs = y_true + np.random.normal(loc, sd, y_true.shape)
    return(y_obs)


def get_data(n, min_x, max_x, sd):
    '''
    ---------------------
    Input:
    Output: 
    ---------------------
    '''
    x = np.random.uniform(min_x, max_x, n)
    
    y_true = get_sin_basis(x)
    y_obs = add_noise(y_true, sd = sd)
    
    return x, y_true, y_obs


def plot_data(x, y_obs, path):
    '''
    ------------------------
    Input: Dataset and degree
    Output: Assignment data
    ------------------------
    '''
    # Close any figures currently open
    plt.clf()

    # Make grids of x and y points to plot
    x_grid = np.linspace(0, 5, 1000000)
    y_grid = np.array([get_sin_basis(example) for example in x_grid])

    # Title of the plot
    title = "True basis function vs. Noisy data points"

    # Plot the true curve and then plot the observed values
    plt.plot(x_grid, y_grid, label = "True function")
    plt.plot(x, y_obs, "r.")
    
    # Add annotations
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title(title)
    
    # Format the axes
    axes = plt.gca()
    axes.set_xlim([0,1.1])
    axes.set_ylim([0,1.1])

    
    # Display and save plot
    plt.show()
    plt.savefig(path)


def plot_regression_predictions(path, title, start_k, end_k, 
                                results, x, y,  x_lab = "X", 
                                y_lab="Y", add_data=True):
    '''
    ------------------------
    Input: Dataset and degree
    Output: Assignment data
    ------------------------
    ''' 
    plt.clf()

    # Create dimensions to iterate over
    dims = range(start_k, end_k + 1)
    
    # Make grids for plot
    x_grid = np.linspace(-5, 5, 100000)
    
    # These iterate through orders/degrees [0 to k-1] using dimension
    x_basis = [get_polynomial_basis(x_grid, dim) for dim in dims]
    y_grid = [get_predictions(basis, result['beta_hat']) for basis, result in zip(x_basis, results)]
    
    # Plots
    for i, y_pred in enumerate(y_grid):
        plt.plot(x_grid, y_pred, label = str(i + start_k))

    # Overlay the observed data if the add_data option is switched on is passed through
    if add_data:
        plt.plot(x, y, "r.")
    
    # Add annotations
    plt.xlabel(x_lab)
    plt.ylabel(y_lab)
    plt.title(title)

    # Add legend
    if not add_data: 
        plt.legend(title="Basis dimension")
    
    # Set the axes
    axes = plt.gca()
    axes.set_xlim([0,1])
    axes.set_ylim([-1.5,1.5])

    
    # Display and save plot
    plt.show()
    plt.savefig(path)


def plot_regression_loss(losses, highest_k, path):
    '''
    ------------------------
    Input: Dataset and degree
    Output: Assignment data
    ------------------------
    '''
    # Close any currently open plots
    plt.clf()

    # Title of the plot
    title = "Polynomial degree vs. training error"

    # Make grids of x and y points to plot
    x_grid = np.arange(1, highest_k + 1)
    
    # Plot the true curve
    plt.plot(x_grid, losses, "r.")
    
    # Add annotations
    plt.xlabel('Polynomial degree')
    plt.ylabel('Log MSE')
    plt.title(title)
    
    # Get current access
    axes = plt.gca()
    axes.set_xlim([0,20])
    axes.set_ylim([min(losses) - 0.1, max(losses) + 0.1])

    # Show plots as a check
    plt.show()
    plt.savefig(path)



def get_test_mse(x_test, y_test, results, k = 18):
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    # Get features
    x_basis = [get_polynomial_basis(x_test, dim) for dim in range(1, k + 1)]
    y_preds = [get_predictions(basis, results[deg]['beta_hat']) for basis, deg in zip(x_basis, range(k + 1))]
    mse_test = [get_mse(y_test, y_pred) for y_pred in y_preds]
    ln_mse_test = [get_ln_mse(mse) for mse in mse_test]

    return(mse_test, ln_mse_test)


def execute_data_plots(x, y, path): 
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    plot_data(x, y, path)


def execute_poly_plots(x, y, path, dims = [2, 5, 10, 12, 14, 18]):
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    title = "Polynomial basis regression results: k = {}"
    
    
    for k in dims:
        fig_title = title.format(k)
        fig_path = path.format(k)
        results = [run_polynomial_regression(k, x, y)]
        plot_regression_predictions(fig_path, fig_title, k, k+1, results, x, y)


def execute_train_loss_plots(x, y, start_dim, end_dim, path):
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    dims = range(start_dim, end_dim + 1)
    results = np.array([run_polynomial_regression(k, x, y) for k in dims])
    ln_mse = np.array([result['ln_mse'] for result in results])
    plot_regression_loss(ln_mse, end_dim, path)

    return(results)


def execute_test_loss_plots(x_test, y_test, results, end_dim, path):
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    mse_test, ln_mse_test = get_test_mse(x_test, y_test, results)
    plot_regression_loss(ln_mse_test, end_dim, path)
    return(ln_mse_test)


def main(path_data_plot =  os.path.join(".", "figs", '1_2_data.png'), 
         path_poly_plot = os.path.join(".", "figs", '1_2_results_dim_{}.png'), 
         path_train_loss = os.path.join(".", "figs", "1_2_train_loss.png"), 
         path_test_loss = os.path.join(".", "figs", '1_2_test_loss.png'),
         path_train_loss_multiple = os.path.join(".", "figs", '1_2_train_loss_100_runs.png'),
         path_test_loss_multiple = os.path.join(".", "figs", '1_2_test_loss_100_runs.png'), 
         n_runs = 1):
    '''
    ---------------------
    Input: Parameters needed for data
    Output: output
    ---------------------
    '''
    
    # Set the random seed to reproduce
    np.random.seed(1291239)

    # Set parameters
    min_x = 0
    max_x = 1 
    sigma = 0.07 
    n_train_samples = 30
    n_test_samples = 1000

    # Store dimensions of regression basis functions
    # Note that these are dimensions and not degrees
    # Degree of polynomial = Dimension of polynomial - 1
    start_dim = 1
    end_dim = 18

    # This is for the initial single run
    if n_runs == 1:
        
        # Get dataset
        x, y_true, y_obs = get_data(n_train_samples, min_x, max_x, sigma)
        x_test, y_test_true, y_test_obs = get_data(n_test_samples, min_x, max_x, sigma)

        # Make plots
        execute_data_plots(x, y_obs, path_data_plot)
        execute_poly_plots(x, y_obs, path_poly_plot)

        # Store plots
        results = execute_train_loss_plots(x, y_obs, start_dim, end_dim, path_train_loss)
        ln_mse_test = execute_test_loss_plots(x_test, y_test_obs, results, end_dim, path_test_loss)

    # This is for multiple runs to return average MSE
    else:
        
        # Create list to store results
        results = []
        
        # Call the process for the no. of runs input by the user
        for counter in range(n_runs):
            
            # Print progress
            print("Doing the {}th run...".format(counter))
            
            # Make new datasets
            x, y_true, y_obs = get_data(n_train_samples, min_x, max_x, sigma)
            x_test, y_test_true, y_test_obs = get_data(n_test_samples, min_x, max_x, sigma)

            # Store dimensions to iterate over and then run polynomial regressions
            dims = range(start_dim, end_dim + 1)
            results_from_single_run = [run_polynomial_regression(k, x, y_obs) for k in dims]

            # Get results on test set
            # First create the testing features
            mse_test, ln_mse_test = get_test_mse(x_test, y_test_obs, results_from_single_run)

            # Append this to results
            for result, mse, ln_mse in zip(results_from_single_run, mse_test, ln_mse_test):
                result['mse_test'] = mse
                result['ln_mse_test'] = ln_mse
                
            # Store results
            results.append(results_from_single_run)

        
        # Store the average
        mse = [np.mean(np.array([results[run][degree]['mse'] for run in range(n_runs)])) for degree in range(end_dim)]
        mse_test = [np.mean(np.array([results[run][degree]['mse_test'] for run in range(n_runs)])) for degree in range(end_dim)]

        # Take logs
        ln_mse = np.log(mse)
        ln_mse_test = np.log(mse_test)

        # Now make plots 
        plot_regression_loss(ln_mse, end_dim, path_train_loss_multiple)
        plot_regression_loss(ln_mse_test, end_dim, path_test_loss_multiple)


    # Return results
    return(results)



if __name__ == '__main__':
    results = main(n_runs=100)