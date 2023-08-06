from matplotlib import pyplot as plt
import numpy as np
from pyLearnAlgorithms.linear_regression import LinearRegression
from pyLearnAlgorithms.polynomial_regression import PolynomialRegression

class GraphView():
    """graphic display class of machine learning models"""

    def __init__(self, X = np.array([]), y = np.array([])):
        """stores predictive attributes and labels"""

        # predictive attributes
        self.X = X
        # values to be predicted
        self.y = y
    
        return None

    def view_data(self, xlabel, ylabel, title):
        """data visualization"""

        plt.figure(figsize = (10, 5))
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)

        return None

    def model_linear(self, xlabel, ylabel, title):
        """plots the graph of the linear regression model"""

        model = LinearRegression(self.X, self.y)
        values = model.trainLinearReg()
        m = self.y.size 
        plt.figure(figsize = (10,5))
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1.5)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.plot(self.X, np.dot(X_bias, values.x), '--', lw=2)

        return None

    def model_linear_normal_equation(self, xlabel, ylabel, title):
        """plots the graph of the linear regression model with normal equation"""

        model = LinearRegression(self.X, self.y)
        _, grad = model.normal_equation()
        m = self.y.size 
        plt.figure(figsize = (10,5))
        X_bias = np.concatenate([np.ones((m, 1)), self.X], axis=1)
        plt.plot(self.X, self.y, 'ro', ms=10, mec='k', mew=1.5)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.plot(self.X, np.dot(X_bias, grad), '--', lw=2)

        return None
    
    def model_poly(self, xlabel, ylabel, title, polynomial_degree, lambda_ = 0.0, maxiter = 200):
        """plots the graph of the polynomial regression model"""

        x = np.arange(np.min(self.X) - 15, np.max(self.X) + 25, 0.05).reshape(-1, 1)
        model_poly = PolynomialRegression(self.X, self.y)
        X_poly = model_poly.polyFeatures(x, polynomial_degree)
        data_poly = model_poly.polyFeatures(self.X, polynomial_degree)
        _, mu, sigma = model_poly.featureNormalize(data_poly)
        X_poly -= mu
        X_poly /= sigma
        X_poly = np.concatenate([np.ones((x.shape[0], 1)), X_poly], axis=1)
        optimized_values = model_poly.trainPolyReg(polynomial_degree, lambda_, maxiter)
        plt.figure(figsize = (10, 5))
        plt.plot(self.X, self.y, 'ro', ms=10, mew=1.5, mec='k')
        plt.plot(x, np.dot(X_poly, optimized_values.x), '--', lw=2)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.title(title)
        plt.ylim([np.min(self.y) - 15, np.max(self.y) + 25])
        
        return None
    
    def validation_curve_poly(self, X_poly, y,Xval, yval, lambda_vec):
        """graphically analyzes the best value of the lambda hyperparameter for normalization"""

        model = PolynomialRegression(self.X, self.y)
        lambda_vec, error_train, error_val = model.validationCurve(X_poly,y,Xval,yval,lambda_vec)
        plt.figure(figsize = (10, 5))
        plt.plot(lambda_vec, error_train, '-o', lambda_vec, error_val, '-o', lw = 2)
        plt.legend(['Train', 'Cross Validation'])
        plt.xlabel('lambda')
        plt.ylabel('Error')

        return None
    
    def learning_curve(self, error_train, erro_val):
        """learning curve for bias vs variance analysis"""

        m = self.y.size 
        plt.figure(figsize = (10, 5))
        plt.plot(np.arange(1, m+1), error_train, np.arange(1, m+1), erro_val, lw=2)
        plt.title('Learning Curve')
        plt.legend(['Training', 'Cross Validation'])
        plt.xlabel('Number of trainable examples')
        plt.ylabel('Error')

        return None
    
    def predicted_values(self, Xtest, ytest, pred):
        """visualization of expected data with that obtained"""

        plt.figure(figsize = (10,5))
        plt.scatter(Xtest, ytest, label = 'correct values')
        plt.scatter( Xtest, pred, label = 'predict values')
        plt.legend()
        plt.grid(True)
        plt.box(False)
        plt.title('Predicted Values')

        return None

    def visualize_image(self, image_array, figsize = (20,6), box = False, title = ''):
        """method for viewing images"""
        
        plt.figure(figsize = figsize)
        plt.imshow(image_array)
        plt.box(box)
        plt.title(title)

        return None
    
    def visualize_benford_law(self, list_prob):
        """method for visualizing the benford curve in images"""
        
        plt.figure(figsize = (10, 5))
        plt.plot([1,2,3,4,5,6,7,8,9], list_prob, '-o')
        plt.title("Benford's Law")
        plt.grid(True)
        plt.box(False)

        return None

    
    


