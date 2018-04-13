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
#test=test.drop(['Date'],axis=1)
train_xy,val = train_test_split(train, test_size = 0.3,random_state=1)

y = train_xy.Accept
X = train_xy.drop(['Accept'],axis=1)
val_y = val.Accept
val_X = val.drop(['Accept'],axis=1)




#给矩阵赋值
xgb_val = xgb.DMatrix(val_X,label=val_y)
xgb_train = xgb.DMatrix(X, label=y)
xgb_test = xgb.DMatrix(test)
xgb_t=xgb.DMatrix(X)

params={
'booster':'gbtree',
'silent':0 ,
'nthread':4,

'eta': 0.05,
'min_child_weight':1,

'max_depth':4,

#'max_leaf_nodes':10,
'max_delta_step':10,
'gamma':0.2,
'subsample':0.6,
'colsample_bytree':0.6,
'lambda':1,
'alpha':3,
'scale_pos_weight':1,



'seed':10,
'eval_metric': 'auc',
'objective': 'binary:logistic',
}

plst = list(params.items())
num_rounds = 5000 # 迭代次数
watchlist = [(xgb_train, 'train'),(xgb_val, 'val')]
#

model = xgb.train(plst, xgb_train, num_rounds, watchlist,early_stopping_rounds=100)
model.save_model('xgb.model') # 用于存储训练出的模型
print("best best_ntree_limit",model.best_ntree_limit)

'''
preds1 = model.predict(xgb_train,ntree_limit=model.best_ntree_limit)
n=0
for i in preds1:
if(i>0.5):
print(i)
n+=1


np.savetxt('xgb_train_output.csv',np.c_[range(1,len(xgb_train)+1),X,preds1],delimiter=',',header='ImageId,Label',comments='')
'''
trains = train.drop(['Accept'],axis=1)
trains1=xgb.DMatrix(trains)
preds = model.predict(xgb_test,ntree_limit=model.best_ntree_limit)
'''
for i in range(len(preds)):
    if(preds[i]>0.5):
        preds[i]=1
    else:
        preds[i]=0
'''
np.savetxt('xgb_submission.csv',np.c_[range(1,len(test)+1),preds],delimiter=',',header='Id,Accept_probility',comments='',fmt="%.4f")

#输出运行时长
cost_time = time.time()-start_time
print ("xgboost success!",'\n',"cost time:",cost_time,"(s)......")