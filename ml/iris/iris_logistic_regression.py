import pandas as pd
import pickle
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, metrics
from sklearn.tree import DecisionTreeClassifier

train = train = pd.read_csv('../datasets/data_train1.csv')
test = test = pd.read_csv('../datasets/data_test1.csv')

train_X = train[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
train_y = train.Species

test_X = test[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
test_y = test.Species

model=LogisticRegression(max_iter=500,
                        fit_intercept=True)
model.fit(train_X,train_y)
prediction=model.predict(test_X)
accuracy=metrics.accuracy_score(prediction,test_y)
print(f"Logistic regression model accuracy is {format(accuracy)}")

# Save to file in the current working directory
pkl_filename = "model/iris_logistic_regression.pkl"
with open(pkl_filename, 'wb') as file:
    pickle.dump(model, file)

# Load from file
with open(pkl_filename, 'rb') as file:
    pickle_model = pickle.load(file)
    
# Calculate the accuracy score and predict target values
score = pickle_model.score(test_X, test_y)
print(f"Test score: {format(100 * score)}")

predict_Y = pickle_model.predict(test_X)
print(f"The prdiction result: {predict_Y}")

# Save testing to CSV
test_X.to_csv('../../data_testing/input_logistic_regression.csv', index=False)

