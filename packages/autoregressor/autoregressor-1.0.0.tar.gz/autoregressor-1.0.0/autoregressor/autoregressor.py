import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from AutoRegressor import compute
from sklearn.metrics import r2_score
import warnings; 
warnings.simplefilter('ignore')


def fillMissing(df):
    df.apply(lambda x: x.fillna(x.mean()),axis=0)
    return df

def scale(X_train ,  y_train):
        scalerX = MinMaxScaler()
        x = scalerX.fit_transform(X_train.values)
        xdf = pd.DataFrame(x , columns = X_train.columns)
        scalerY = MinMaxScaler()
        y = scalerX.fit_transform(np.array(y_train).reshape(-1 , 1))
        ydf = pd.DataFrame(y)
        return xdf , ydf 
    
def inverse_scale(y_train ,  pred):
        scalerY = MinMaxScaler()
        y = scalerY.fit_transform(np.array(y_train).reshape(-1 , 1))
        scaled_pred = scalerY.inverse_transform(pred)
        ydf = pd.DataFrame(scaled_pred)
        return  ydf 

def solve(X , y , X_test):
    X = fillMissing(X)
#     y = fillMissing(y)
    X_test = fillMissing(X_test)
    X_scaled , y_scaled = scale(X , y)
    X_test_scaled = MinMaxScaler().fit_transform(X_test)
    model = compute.compute(X_scaled , y_scaled)
    model.fit(X_scaled , y_scaled)
    print(model.score(X_scaled , y_scaled))
    pred = model.predict(X_test_scaled)
    pred_scaled = inverse_scale(y , np.array(pred).reshape(1 , -1))
    return pred_scaled.transpose()
    
