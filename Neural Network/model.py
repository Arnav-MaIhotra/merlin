from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve, precision_recall_curve
from sklearn.preprocessing import StandardScaler

plt.style.use('dark_background')

buys = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v2\buy_metrics_v2.csv")

X_buys = buys[["P/E Ratio", "P/B Ratio"]]

clf = IsolationForest(contamination=0.1)

clf.fit(X_buys)

outliers = clf.predict(X_buys)

X_buys = X_buys[outliers != -1]

ones = np.ones(len(X_buys))

sells = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\v2\sell_metrics_v2.csv")

X_sells = sells[["P/E Ratio", "P/B Ratio"]]

clf.fit(X_sells)

outliers = clf.predict(X_sells)

X_sells = X_sells[outliers != -1]

zeros = np.zeros(len(X_sells))

X = np.concatenate((X_buys, X_sells))

y = np.concatenate((ones, zeros))

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.33, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

accuracy_default = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy_default}")

y_probs = model.predict_proba(X_test)

print(y_probs)

conf_matrix = confusion_matrix(y_test, y_pred)
report = classification_report(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_probs[:, 1])

fpr, tpr, _ = roc_curve(y_test, y_probs[:, 1])
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})")
plt.plot([0, 1], [0, 1], 'k--', label="Random Guess")
plt.xlabel("False Positive Rate")
plt.ylabel("True Positive Rate")
plt.legend()
plt.show()

print(conf_matrix)
print(report)
print(roc_auc)

print(model.coef_)