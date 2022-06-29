# Home-Credit-Default-Risk

Predicting the risk of default for customers applied for loan at Home Credit as a classification problem. 

A project with a rather large amount of data from internal and external sources. Here the goal is to find hints in the customer's financial history which can help predict the risk of that customer's default.

Extensive EDA has been done to extract some information from different datasets. lightgbm, XGBoost and PyTorch has been used as models for classification. Pytorch with softmax performed the worst and XGBoost performed best with AUC score of 0.79020. 
ensemble of lgbm and XGBoost didn't improve the score and final score was 0.79020.
