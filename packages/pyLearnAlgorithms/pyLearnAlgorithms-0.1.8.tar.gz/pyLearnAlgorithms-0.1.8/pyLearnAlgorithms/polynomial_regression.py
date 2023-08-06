import numpy as np
from pyLearnAlgorithms.linear_regression import LinearRegression 
from scipy import optimize

class PolynomialRegression():
    """class for building polynomial regression models"""
    
    def __init__(self, X, y):

            # predictive attributes
            self.X = X
            # values to be predicted
            self.y = y

            return None

    def polyFeatures(self, X, polynomial_degree = 1):
        """performs polynomial mapping on predictive attributes"""

        X_poly = np.zeros((X.shape[0], polynomial_degree))
        for i in range(polynomial_degree):
            X_poly[:, i] = X[:, 0] ** (i + 1)

        return X_poly
    
    def featureNormalize(self, X):
        """performs normalization on predictive attributes by normal distribution"""
    
        mu = np.mean(X, axis = 0)
        X_norm = (X - mu)
        sigma = np.std(X_norm, axis = 0, ddof = 1)
        X_norm = X_norm / sigma
        m = self.y.size 
        X_norm = np.concatenate([np.ones((m, 1)), X_norm], axis=1)
        
        return X_norm, mu, sigma

    def prepareExtracts(self, extractX, extractY, polynomial_degree):
        """performs normalization and polynomial mapping on other data extracts"""

        model = PolynomialRegression(self.X, self.y)
        X_poly = model.polyFeatures(extractX, polynomial_degree)
        data_poly = model.polyFeatures(self.X, polynomial_degree)
        _, mu, sigma = model.featureNormalize(data_poly)
        X_poly -= mu
        X_poly /= sigma
        X_poly = np.concatenate([np.ones((extractY.size, 1)), X_poly], axis=1)

        return X_poly

    def trainLinearReg(self, polynomial_degree, lambda_ = 0.0, maxiter = 200):
        """training the model for minimizing the cost function and modifying theta parameters"""

        model_poly = PolynomialRegression(self.X, self.y)
        X_poly = model_poly.polyFeatures(self.X, polynomial_degree)
        X_poly, _, _ = model_poly.featureNormalize(X_poly)
        teta_inicial = np.zeros(X_poly[0,:].size)
        X_poly = np.delete(X_poly, 0, 1)
        model_linear = LinearRegression(X_poly, self.y)
        costFunction = lambda t: model_linear.linearRegCostFunction(t, lambda_)
        options = {'maxiter': maxiter}
        res=optimize.minimize(costFunction,teta_inicial,jac=True,method='TNC',options=options)

        return res
    
    def __linearRegCostFunction(self, X, y, theta = [1,1], lambda_= 0.0):
        """cost function for a varied hypothesis (with regularization)"""

        theta = np.array(theta)
        m = y.size 
        J = 0
        grad = np.zeros(theta.shape)
        h = X.dot(theta)
        J = (1/(2*m))*np.sum(np.square(h-y))+(lambda_/(2*m))*np.sum(np.square(theta[1:]))
        grad = (1/m)*(h-y).dot(X)
        grad[1:] = grad[1:] + (lambda_/m)*theta[1:]

        return J, grad
    
    def __trainLinearReg(self,X, y, lambda_ = 0.0, maxiter = 200):
        """training the model for minimizing the cost function and modifying theta parameters"""

        teta_inicial = np.zeros(X.shape[1])
        costFunction = lambda t: self.__linearRegCostFunction(X, y, t, lambda_)
        options = {'maxiter': maxiter}
        res = optimize.minimize(costFunction,teta_inicial,jac=True,method='TNC',options=options)

        return res
    
    def learningCurve(self, X_poly, y, Xval, yval, lambda_ = 0.0):
        """computes training error and validation error for different data extracts"""
        
        m = y.size
        error_train = np.zeros(m)
        error_val   = np.zeros(m)
        for i in range(1, m + 1):
            teta_t = self.__trainLinearReg(X_poly[:i], y[:i], lambda_)
            error_train[i-1],_=self.__linearRegCostFunction(X_poly[:i], y[:i],teta_t.x, lambda_)
            error_val[i - 1], _ = self.__linearRegCostFunction(Xval, yval, teta_t.x, lambda_)
            
        return error_train, error_val
    
    def validationCurve(self,X_poly,y,Xval,yval,lambda_vec=[0,0.001,0.003,0.01,0.03,0.1,0.3,1,3,10]):
        """analyzes the lambda values for the best normalization"""

        error_train = np.zeros(len(lambda_vec))
        error_val = np.zeros(len(lambda_vec))
        for i in range(len(lambda_vec)):
            lambda_try = lambda_vec[i]
            teta_t = self.__trainLinearReg(X_poly, y, lambda_ = lambda_try)
            error_train[i], _ = self.__linearRegCostFunction(X_poly, y, teta_t.x, lambda_ = 0)
            error_val[i], _ = self.__linearRegCostFunction(Xval, yval, teta_t.x, lambda_ = 0)

        return lambda_vec, error_train, error_val
    
    # problem =====
    '''def predict(self, X_poly, y, lambda_ = 0.0, Xtest):
        """makes the prediction for the test values"""

        teta_t = self.__trainLinearReg(X_poly, y, lambda_)
        X_bias = np.concatenate([np.ones((Xtest.size, 1)), Xtest], axis=1)
        pred = np.dot(X_bias, teta_t.x)

        return pred ''' 

    



    