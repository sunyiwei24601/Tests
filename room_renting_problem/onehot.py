import pandas as pd
import numpy as np
train=pd.read_csv('case2_training_onehot.csv')
t=pd.get_dummies(train)
print(t.dtypes)