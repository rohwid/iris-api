from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

import pickle
import pandas as pd

app = Flask(__name__)

dataset = load_iris()
data = pd.DataFrame(dataset['data'], columns = ["Petal length","Petal Width","Sepal Length","Sepal Width"])
data['Species'] = dataset['target']
data['Species'] = data['Species'].apply(lambda x: dataset['target_names'][x])

train, test = train_test_split(data, test_size = 0.3)

train_X = train[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
train_y = train.Species

test_X = test[["Sepal Length", "Sepal Width", "Petal length", "Petal Width"]]
test_y = test.Species

with open('iris_svm.pkl', 'rb') as file:
    svm_pickle_model = pickle.load(file)

with open('iris_logistic_regression.pkl', 'rb') as file:
    lr_pickle_model = pickle.load(file)

with open('iris_decission_tree.pkl', 'rb') as file:
    dt_pickle_model = pickle.load(file)

@app.route('/testing',methods=['POST'])
def predict():
    request_data = request.get_json()

    data_testing = {
        'Sepal Length': request_data['Sepal Length'],
        'Sepal Width': request_data['Sepal Width'],
        'Petal Length': request_data['Petal Length'],
        'Petal Width': request_data['Petal Width']
    }

    svm_score = svm_pickle_model.score(test_X, test_y)
    lr_score = lr_pickle_model.score(test_X, test_y)
    dt_score = dt_pickle_model.score(test_X, test_y)

    svm_predict = svm_pickle_model.predict(pd.DataFrame(data_testing))
    lr_predict = lr_pickle_model.predict(pd.DataFrame(data_testing))
    dt_predict = dt_pickle_model.predict(pd.DataFrame(data_testing))

    model_score = [svm_score, lr_score, dt_score]
    max_score = max(model_score)

    result = [i for i, j in enumerate(model_score) if j == max_score]

    if (len(result) > 1):
        select = random.choice(result)
    else:
        select = result[0]

    if (select == 0):
        return jsonify(svm_predict.tolist())
    elif (select == 1):
        return jsonify(lr_predict.tolist())
    elif (select == 2):
        return jsonify(dt_predict.tolist())

app.run(port=5000, debug=True)