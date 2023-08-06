import pandas as pd
from sklearn.model_selection import GridSearchCV
from sklearn import svm
from sklearn.cross_decomposition import PLSRegression
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import BayesianRidge
from sklearn.linear_model import ElasticNetCV
from sklearn.linear_model import TheilSenRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import VotingRegressor

def bestSVR(X_train , y_train):
    param_grid = {'C': [1.0 , 1.4 , 1.8 , 2.2 , 2.6 , 3.0],  
              'gamma': [0.3, 0.1,0.03, 0.01,0.003], 
              'kernel': ['rbf' , 'linear']}  
    grid = GridSearchCV(svm.SVR(), param_grid, refit = True, verbose = 0)
    grid.fit(X_train , y_train)
    return grid.best_estimator_

def bestRandomForest(X_train , y_train):
    param_grid = {
        'n_estimators' : [70 , 85 , 100 , 115 , 130],
        'criterion' : ['mse', 'mae'],
        'max_features' : ['auto' , 'sqrt' , 'log2'],
        'n_jobs' : [1 , -1],
        'warm_start' : [True , False]
    }
    grid = GridSearchCV(RandomForestRegressor(), param_grid, refit = True, verbose = 0)
    grid.fit(X_train , y_train)
    return grid.best_estimator_

def bestKNN(X_train , y_train):
    param_grid = {'n_neighbors': [3 , 5 , 7 , 9],  
              'weights': ['uniform' , 'distance'],
                 'algorithm' : ['auto' , 'ball_tree' , 'kd_tree' , 'brute'],
                 'leaf_size' : [27 , 30 , 33 , 36],
                 'p' : [1 , 2],
                 'n_jobs' : [1 , -1]}
    grid = GridSearchCV(KNeighborsRegressor(), param_grid,refit = True, verbose = 0)
    grid.fit(X_train , y_train)
    return grid.best_estimator_

def bestBayesianRidge(X_train , y_train):
    param_grid = {'n_iter' : [230 , 260 , 300 , 340 , 380],
                 'normalize' : ['True' , 'False']}
    grid = GridSearchCV(BayesianRidge(), param_grid, refit = True, verbose = 0)
    grid.fit(X_train , y_train)
    return grid.best_estimator_

def bestDecisionTree(X_train , y_train):
    param_grid = {
        'criterion' : ['mse', 'friedman_mse', 'mae'],
        'splitter' : ['best' , 'random'],
        'max_features' : ['auto', 'sqrt', "log2"]
    }
    grid = GridSearchCV(DecisionTreeRegressor(), param_grid, refit = True, verbose = 0)
    grid.fit(X_train , y_train)
    return grid.best_estimator_

def compute(X_train , y_train):
    model1 = bestSVR(X_train , y_train)
    model2 = bestRandomForest(X_train , y_train)
    model3 = bestKNN(X_train , y_train)
    model4 = bestBayesianRidge(X_train , y_train)
    model7 = bestDecisionTree(X_train , y_train)
    model = VotingRegressor(estimators = [('random' , model2),('svr' , model1),('knn' , model3),  ('decision' , model7) , ('bayesian' , model4)] , n_jobs = -1)
    return model