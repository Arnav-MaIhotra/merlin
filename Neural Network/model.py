from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, roc_curve
from sklearn.preprocessing import StandardScaler
from itertools import combinations

buys = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v3\buy_metrics_v3.csv")
buys = buys.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
X_buys = buys[["P/E Ratio", "P/B Ratio", "Altman Z-Score"]]

clf = IsolationForest(contamination=0.1)
clf.fit(X_buys)
outliers = clf.predict(X_buys)
X_buys = X_buys[outliers != -1]
ones = np.ones(len(X_buys))

sells = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v3\sell_metrics_v3.csv")
sells = sells.replace([np.inf, -np.inf], np.nan).dropna(axis=0)
X_sells = sells[["P/E Ratio", "P/B Ratio", "Altman Z-Score"]]

clf.fit(X_sells)
outliers = clf.predict(X_sells)
X_sells = X_sells[outliers != -1]
zeros = np.zeros(len(X_sells))

X = np.concatenate((X_buys, X_sells))
y = np.concatenate((ones, zeros))

scaler = StandardScaler()

features = ["P/E Ratio", "P/B Ratio", "Altman Z-Score"]
feature_combinations = []
for i in range(1, len(features) + 1):
    feature_combinations.extend(combinations(features, i))

plt.figure(figsize=(10, 8))

for combo in feature_combinations:
    X_buys_selected = X_buys[list(combo)]
    X_sells_selected = X_sells[list(combo)]
    
    X_selected = np.concatenate((X_buys_selected, X_sells_selected))
    y_selected = np.concatenate((ones, zeros))
    
    X_scaled = scaler.fit_transform(X_selected)
    
    X_train, X_test, y_train, y_test = train_test_split(X_scaled, y_selected, test_size=0.2, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    y_probs = model.predict_proba(X_test)
    fpr, tpr, _ = roc_curve(y_test, y_probs[:, 1])
    roc_auc = roc_auc_score(y_test, y_probs[:, 1])
    
    label = f"{' + '.join(combo)} (AUC = {roc_auc:.2f})"
    plt.plot(fpr, tpr, label=label)

plt.plot([0, 1], [0, 1], 'k--', label="Random Guess")

plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.title("ROC Curves for Different Feature Combinations")
plt.legend(loc="lower right")
plt.show()
