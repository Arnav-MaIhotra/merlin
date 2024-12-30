library(data.table)
library(dplyr)
library(ggplot2)
library(caret)
library(e1071)
library(glmnet)
library(solitude)

theme_set(theme_dark())

buys <- fread("C:/Users/arnav/OneDrive/Documents/Merlin/Neural Network/v2/buy_metrics_v2.csv")
sells <- fread("C:/Users/arnav/OneDrive/Documents/Merlin/Neural Network/v2/sell_metrics_v2.csv")

X_buys <- buys %>% select(`P/E Ratio`, `P/B Ratio`)
X_sells <- sells %>% select(`P/E Ratio`, `P/B Ratio`)

clf_buys <- isolation.forest(X_buys, ntrees = 100)
outliers_buys <- predict(clf_buys, X_buys)
X_buys <- X_buys[outliers_buys == 1, ]

clf_sells <- isolation.forest(X_sells, ntrees = 100)
outliers_sells <- predict(clf_sells, X_sells)
X_sells <- X_sells[outliers_sells == 1, ]

ones <- rep(1, nrow(X_buys))
zeros <- rep(0, nrow(X_sells))

# Combine data
X <- rbind(as.matrix(X_buys), as.matrix(X_sells))
y <- c(ones, zeros)

# Standardize features
scaler <- preProcess(X, method = "scale")
X_scaled <- predict(scaler, X)

# Split data into train and test sets
set.seed(42)
train_index <- createDataPartition(y, p = 0.67, list = FALSE)
X_train <- X_scaled[train_index, ]
X_test <- X_scaled[-train_index, ]
y_train <- y[train_index]
y_test <- y[-train_index]

model <- glmnet(X_train, y_train, family = "binomial", alpha = 0)

y_pred <- predict(model, X_test, type = "class")
y_probs <- predict(model, X_test, type = "response")

accuracy_default <- mean(as.numeric(y_pred) == y_test)
print(paste("Accuracy:", accuracy_default))

conf_matrix <- confusionMatrix(as.factor(y_pred), as.factor(y_test))
print(conf_matrix)

roc_obj <- roc(as.numeric(y_test), as.numeric(y_probs))
auc_value <- auc(roc_obj)
print(paste("AUC:", auc_value))

ggplot(data.frame(fpr = 1 - roc_obj$specificities, tpr = roc_obj$sensitivities)) +
  geom_line(aes(x = fpr, y = tpr), color = "blue") +
  geom_abline(slope = 1, intercept = 0, linetype = "dashed", color = "red") +
  ggtitle(paste("ROC Curve (AUC =", round(auc_value, 2), ")")) +
  xlab("False Positive Rate") +
  ylab("True Positive Rate")

coef_matrix <- as.matrix(coef(model))
print(coef_matrix)