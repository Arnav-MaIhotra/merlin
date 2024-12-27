from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import IsolationForest
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report, roc_auc_score, roc_curve, precision_recall_curve
from sklearn.preprocessing import StandardScaler

plt.style.use('dark_background')

buys = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\buy_metrics_v1.csv")

pe_buys = buys["P/E Ratio"].values.reshape(-1, 1)

clf = IsolationForest(contamination=0.1)

clf.fit(pe_buys)

outliers = clf.predict(pe_buys)

pe_buys = pe_buys[outliers != -1]

ones = np.ones((pe_buys.shape))

sells = pd.read_csv(r"C:\Users\arnav\OneDrive\Documents\Merlin\Neural Network\sell_metrics_v1.csv")

pe_sells = sells["P/E Ratio"].values.reshape(-1, 1)

clf.fit(pe_sells)

outliers = clf.predict(pe_sells)

pe_sells = pe_sells[outliers != -1]

zeros = np.zeros((pe_sells.shape))

X = np.concatenate((pe_buys, pe_sells))

y = np.concatenate((ones, zeros))

plt.figure(1)

plt.scatter(range(len(pe_buys)), pe_buys, color='#B0B0B0', label='Buys')
plt.scatter(range(len(pe_sells)), pe_sells, color='#EEEEEE', label='Sells')
plt.xlabel('Index', color="grey")
plt.ylabel('P/E Ratio', color="grey")
plt.legend(facecolor='black', edgecolor='grey', labelcolor='grey')

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.33, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

y_probs = model.predict_proba(X_test)[:, 1]

y_pred_default = (y_probs >= 0.5).astype(int)
accuracy_default = accuracy_score(y_test, y_pred_default)
print(f"Default Threshold Accuracy: {accuracy_default}")

threshold = 0.4
y_pred_custom = (y_probs >= threshold).astype(int)

accuracy_custom = accuracy_score(y_test, y_pred_custom)
conf_matrix = confusion_matrix(y_test, y_pred_custom)
report = classification_report(y_test, y_pred_custom)
roc_auc = roc_auc_score(y_test, y_probs)

print(accuracy_custom)
print(conf_matrix)
print(report)
print(roc_auc)

plt.figure(2)

fpr, tpr, _ = roc_curve(y_test, y_probs)
plt.plot(fpr, tpr, label=f"ROC Curve (AUC = {roc_auc:.2f})", color="grey")
plt.plot([0, 1], [0, 1], 'k--', label='Random Guess', color="white")
plt.xlabel('False Positive Rate', color="grey")
plt.ylabel('True Positive Rate', color="grey")
plt.title('ROC Curve', color="grey")
plt.legend(facecolor='black', edgecolor='grey', labelcolor='grey')

plt.figure(3)

precision, recall, _ = precision_recall_curve(y_test, y_probs)
plt.plot(recall, precision, label="Precision-Recall Curve", color="grey")
plt.xlabel('Recall', color="grey")
plt.ylabel('Precision', color="grey")
plt.title('Precision-Recall Curve', color="grey")
plt.legend(facecolor='black', edgecolor='grey', labelcolor='grey')
plt.show()