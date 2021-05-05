from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

import random
import pickle
import pandas as pd

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:iris123@0.0.0.0:30000/iris_db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

class Iris(db.Model):
    __tablename__ = 'class_result'
    id = db.Column(db.Integer, primary_key=True)
    method = db.Column(db.String(50), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)

    def __init__(self, method, accuracy):
        self.method = method
        self.accuracy = accuracy


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

    accuracy = 0
    method = "NaN"

    if (select == 0):
        method = "SVM"
        accuracy = svm_score
        
        return jsonify({'method': method, 'accuracy': accuracy})
    
    if (select == 1):
        method = "Logistic Regression"
        accuracy = lr_score
        
        return jsonify({'method': method, 'accuracy': accuracy})
    
    if (select == 2):
        method = "Decision Tree"
        accuracy = dt_score
        
        return jsonify({'method': method, 'accuracy': accuracy})
    
    entry = Iris(method, accuracy)
    db.session.add(entry)
    db.session.commit()


if __name__ == '__main__':
    db.create_all()
    app.run(host = '0.0.0.0', debug = True, port = '5000')