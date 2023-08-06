# forestknn
Explainability of Decision Tree Ensembles (DTE) using Adaptive Nearest Neighbors (AdaptiveNN) Interpretation. 

The explainer uses the AdaptiveNN interpretation to decompose a DTE's prediction into a weighted average of the training data labels. It returns the k-nearest neighbors of the prediction in the form of the k training data points with highest weight. These can then be inspected along with the prediction data to gain insights into the DTE and used for model debugging.

Currently the library supports Scikit-learn's RandomForest - support for popular boosting libraries (LightGBM, XGBoost, CatBoost) is planned.
