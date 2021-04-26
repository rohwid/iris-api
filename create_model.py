import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn import svm, metrics
from sklearn.tree import DecisionTreeClassifier

dataset = load_iris()
data = pd.DataFrame(dataset['data'], columns = ["Petal length","Petal Width","Sepal Length","Sepal Width"])
data['Species'] = dataset['target']
data['Species'] = data['Species'].apply(lambda x: dataset['target_names'][x])

train, test = train_test_split(data, test_size = 0.3)

train_X = train[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
train_y = train.Species

test_X = test[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
test_y = test.Species