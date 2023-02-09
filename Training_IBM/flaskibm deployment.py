from flask import Flask, render_template, request
import numpy as np
import requests
import json

# NOTE: you must manually set API_KEY below using information retrieved from your IBM Cloud account.
API_KEY = "<your API key>"
token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey":
 API_KEY, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
mltoken = token_response.json()["access_token"]

header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}

app = Flask(__name__)
@app.route("/")
def about():
    return render_template('home.html')

@app.route("/predict")
def Predict():
    return render_template('predict.html')


@app.route("/pred", methods=['POST','GET'])
def predict():
    pH = request.form['pH']
    Temprature= request.form['Temprature']
    Taste = request.form['Taste']
    Odor= request.form['Odor']
    Fat = request.form['Fat']
    Turbidity = request.form['Turbidity']
    Colour = request.form['Colour']
    total = [[float(pH), int(Temprature), int(Taste), int(Odor),int(Fat),int(Turbidity), int(Colour)]]
    print(total)
    
    # NOTE: manually define and pass the array(s) of values to be scored in the next line
    payload_scoring = {"input_data": [{"field": [["pH","Temprature", "Taste","Odor", "Fat","Turbidity","Colour"]], "values": [[8.5,70,1,1,1,1,246]]}]}

    response_scoring = requests.post('https://us-south.ml.cloud.ibm.com/ml/v4/deployments/0bd663be-6952-4f16-98cb-e32ab6539c8d/predictions?version=2023-01-30', json=payload_scoring,
    headers={'Authorization': 'Bearer ' + mltoken})
    print("Scoring response")
    print(response_scoring.json())

    print(predictions)
    pred=predictions['predictions'][0]['values'][0][0]

    
    return render_template('submit.html', prediction_text=pred)

if __name__ == "__main__":
    app.run(debug=False)