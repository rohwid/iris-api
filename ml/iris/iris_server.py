from flask import Flask, request, jsonify
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

import os.path
import datetime
import json
import pickle
import pandas as pd
import random

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

with open('model/iris_svm.pkl', 'rb') as file:
    svm_pickle_model = pickle.load(file)

with open('model/iris_logistic_regression.pkl', 'rb') as file:
    lr_pickle_model = pickle.load(file)

with open('model/iris_decission_tree.pkl', 'rb') as file:
    dt_pickle_model = pickle.load(file)

def json_converter(json_data):
    if isinstance(json_data, datetime.datetime):
        return json_data.__str__()

def write_json(input_data, flag):
    if (flag == 0):
        data = {'testing_result': [input_data]}
        
        # Serializing json 
        json_object = json.dumps(data, indent = 4)
        
        # Writing to sample.json
        with open("output/output.json", "w") as outfile:
            outfile.write(json_object)
    else:
        # Serializing json 
        json_object = json.dumps(input_data, indent = 4)
        
        # Writing to sample.json
        with open("output/output.json", "w") as outfile:
            outfile.write(json_object)

def write_output(input_data):
    if os.path.isfile('output/output.json'):    
        with open('output/output.json') as json_file:
            data = json.load(json_file)
            data['testing_result'].append(input_data)
            
        write_json(data, 1)
    else:
        write_json(input_data, 0)

@app.route('/testing', methods=['POST'])
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
    
    test_result = {
        'timestamp': json_converter(datetime.datetime.now()),
        'method': "NaN",
        'accuracy': 0
    }
    
    if (select == 0):
        test_result['method'] = "SVM"
        test_result['accuracy'] = svm_score
        write_output(test_result)
        
        return jsonify(test_result)
    
    if (select == 1):
        test_result['method'] = "Linear Logistic"
        test_result['accuracy'] = lr_score
        write_output(test_result)
        
        return jsonify(test_result)
    
    if (select == 2):
        test_result['method'] = "Decision Tree"
        test_result['accuracy'] = dt_score
        write_output(test_result)
        
        return jsonify(test_result)
    
if __name__ == '__main__':
    app.run(host = '0.0.0.0', debug = True, port = '5000')