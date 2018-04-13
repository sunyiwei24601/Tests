import sklearn
import xgboost as xgb
import pandas as pd
import numpy as np
from sklearn.cross_validation import train_test_split
import time
from itertools import product
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestRegressor
from sklearn import neighbors










trains=pd.read_csv('case2_training.csv')
test=pd.read_csv('case2_testing.csv')
train,val = train_test_split(trains, test_size = 0.3,random_state=2)



label=train.Accept
train=train.drop(['Accept'],axis=1)
val_label=val.Accept
val=val.drop(['Accept'],axis=1)


clf=neighbors.KNeighborsClassifier(n_neighbors=4,algorithm='brute',p=2,leaf_size=50)



clf.fit(train,label)

trains=trains.drop(['Accept'],axis=1)
preds=clf.predict(val)

for i in range(len(preds)):
    if preds[i]>0.5:
        preds[i]=1
    else:
        preds[i]=0

n=0
val_list=list(val_label)
for i in range(len(preds)):
    if preds[i]==val_list[i:i+1]:
        n+=1
print("交叉检验结果为："+str(n/15000))


np.savetxt('skl_submission.csv',np.c_[range(1,len(val)+1),preds],delimiter=',',header='ImageId,Label',comments='',fmt="%d")
