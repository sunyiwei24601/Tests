import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
import time

start_time = time.time()
train=pd.read_csv('case2_training_onehot.csv')
test=pd.read_csv('case2_testing_onehot.csv')
train=pd.get_dummies(train)
test=pd.get_dummies(test)
X=train.drop(['Accept'],axis=1)
y=train.Accept

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.1, random_state=1729)
print(X_train.shape, X_test.shape)

#模型参数设置
xlf = xgb.XGBRegressor(
                        max_depth=10,
                        eta=0.01,
                        learning_rate=0.1,
                        n_estimators=500,
                        silent=0,
                        objective='binary:logistic',
                        nthread=-1,
                        gamma=0,
                        min_child_weight=1,
                        max_delta_step=0,
                        subsample=0.85,
                        colsample_bytree=0.7,
                        colsample_bylevel=1,
                        reg_alpha=0,
                        reg_lambda=1,
                        scale_pos_weight=1,
                        seed=1440,
                        missing=None)
xlf.fit(X_train, y_train, eval_metric='auc', verbose = True, eval_set = [(X_test, y_test)],early_stopping_rounds=100)