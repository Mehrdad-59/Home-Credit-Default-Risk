# -*- coding: utf-8 -*-
"""Home Credit Default Risk_Enesmble0.79020.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1gcYrm2MpmO-Hnkjpyl2LU0JgpTyIwAeV
"""

import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score

def AUC(y_true, y_score):
  return roc_auc_score(y_true, y_score)

#! gdown 1oOYKhDY_sTs4Qt0dluKCnUZAAUDazSmn

#! gdown 1dVTuMbcQwYppTr9LeGe3-Aq7EAB0N7qH

#train=pd.read_csv('HC_train.csv')
#y=train['TARGET']

preds_lgb=np.load('pred_lgb.npy')
val_preds_lgb=np.load('val_pred_lgb.npy')
preds_XGB=np.load('pred_XGB.npy')
val_preds_XGB=np.load('val_pred_XGB.npy')

xgb_coef=0.9
lgb_coef=0.1

ensemble_preds=(lgb_coef*preds_lgb)+(xgb_coef*preds_XGB)
ensemble_val_preds=(lgb_coef*val_preds_lgb)+(xgb_coef*val_preds_XGB)

#def to_labels(pos_probs, threshold):
#	return (pos_probs >= threshold).astype('int')
 
#thresholds = np.arange(0, 1, 0.001)
#scores = [AUC(y, to_labels(ensemble_val_preds, t)) for t in thresholds]
#ix = np.argmax(scores)
#print('Threshold=%.3f, AUC=%.5f' % (thresholds[ix], scores[ix]))

#ensemble_preds=np.where(ensemble_preds<thresholds[ix], 0, 1)

submission=pd.read_csv('sample_submission.csv')

submission['TARGET']=ensemble_preds

submission.to_csv('submission_ensemble.csv', index=False)

from google.colab import files

files.download('submission_ensemble.csv')