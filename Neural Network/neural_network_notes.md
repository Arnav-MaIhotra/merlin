# Neural Network Notes

- Combine as many relevent metrics as possible into a binary classification system
- Possible model choices include feedforward neural networks, multilayer perceptrons, and support vector machine - neural network hybrids

---

**Current Metrics**

- P/E ratio: kind of useless right now, maybe try pct change or deviation from industry mean in future
- P/B ratio: ended up hurting a logistic regression model (maybe will help with a neural network), maybe try pct change or deviation from 1 in future
- Altman z-score: was kind of useful, logistic regression gave larger cap (higher z-score usually) companies better rankings which isn't wanted, but neural network might change