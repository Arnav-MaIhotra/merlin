using CSV
using DataFrames
using MLJ
using Plots
using Statistics
using ScikitLearn
using ScikitLearn: @sk_import
using Random

Plots.gr(fmt=:png, color=:black)

buys = CSV.File("C:\\Users\\arnav\\OneDrive\\Documents\\Merlin\\Neural Network\\v2\\buy_metrics_v2.csv") |> DataFrame
sells = CSV.File("C:\\Users\\arnav\\OneDrive\\Documents\\Merlin\\Neural Network\\v2\\sell_metrics_v2.csv") |> DataFrame

X_buys = buys[!, ["P/E Ratio", "P/B Ratio"]]
clf = ScikitLearn.IsolationForest(contamination=0.1)
fit!(clf, X_buys)
outliers_buys = predict(clf, X_buys)
X_buys = X_buys[outliers_buys .!= -1, :]
ones = ones(length(X_buys))

X_sells = sells[!, ["P/E Ratio", "P/B Ratio"]]
fit!(clf, X_sells)
outliers_sells = predict(clf, X_sells)
X_sells = X_sells[outliers_sells .!= -1, :]
zeros = zeros(length(X_sells))

X = vcat(Matrix(X_buys), Matrix(X_sells))
y = vcat(ones, zeros)

scaler = StandardScaler()
X_scaled = fit_transform(scaler, X)

train_idx, test_idx = train_test_split(1:length(y), test_size=0.33, random_state=42)
X_train = X_scaled[train_idx, :]
y_train = y[train_idx]
X_test = X_scaled[test_idx, :]
y_test = y[test_idx]

model = @sk_import linear_model:LogisticRegression
fit!(model, X_train, y_train)

y_pred = predict(model, X_test)
accuracy_default = mean(y_pred .== y_test)
println("Accuracy: ", accuracy_default)

y_probs = predict_proba(model, X_test)

println("Predicted Probabilities: ", y_probs)

conf_matrix = confusion_matrix(y_test, y_pred)
println("Confusion Matrix: ", conf_matrix)

roc_auc = roc_auc_score(y_test, y_probs[:, 2])
println("ROC AUC: ", roc_auc)

fpr, tpr, _ = roc_curve(y_test, y_probs[:, 2])
plot(fpr, tpr, label="ROC Curve (AUC = $roc_auc)")
plot!([0, 1], [0, 1], linestyle=:dash, label="Random Guess")
xlabel!("False Positive Rate")
ylabel!("True Positive Rate")
legend!(:topright)

println("Classification Report: ", classification_report(y_test, y_pred))

println("Model Coefficients: ", model.coef_)