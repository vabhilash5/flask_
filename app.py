
from flask import Flask, render_template, request, app, url_for
from pandas import to_datetime
import requests
import pickle
import numpy as np
import datetime
# from sklearn.preprocessing import 

app = Flask(__name__)
model = pickle.load(open('flight_rf1.pkl','rb'))

@app.route('/')

def home():
    return render_template('index.html')

@app.route('/predict',methods=['POST'])

def predict():
    data= [x for x in request.form.values()]
    airline= [ 'Air India', 'GoAir', 'IndiGo', 'Jet Airways', 'Jet Airways Business','Multiple carriers','Multiple carriers Premium economy', 'SpiceJet', 'Trujet','Vistara', 
       'Vistara Premium economy']
    Airline = data[0]
    lst_2=[0,0,0,0,0,0,0,0,0,0,0]
    if Airline!='Air Asia':
        lst_2[airline.index(Airline)]=1

    city= ['Banglore', 'Chennai', 'Delhi', 'Kolkata','Mumbai']
    source = data[1]
    lst=[0,0,0,0]
    if source!='Banglore':
        lst[city.index(source)-1]=1

    des_city = ['Banglore','Cochin','Delhi', 'Hyderabad' ,'Kolkata','New Delhi']
    destination = data[2]
    lst1=[0,0,0,0,0]
    if destination!='Banglore':
        lst1[des_city.index(destination)-1]=1

    total_stops = data[3]

    dep_date= data[4][:10]
    dep_time= data[4][-4:]
    format= '%Y-%m-%dT%H:%M'
    dep_date = datetime.datetime.strptime(data[4], format)
    # dep_time= datetime.time(dep_time)
    # dep = datetime.datetime.combine(dep_date,dep_time)

    arr_date= data[5][:10]
    arr_time= data[5][-4:]
    arr_date = datetime.datetime.strptime(data[5], format)
    # arr_time= datetime.time(arr_time)
    # arr = datetime.datetime.combine(arr_date,arr_time)

    dep_hrs = dep_date.hour
    arr_hrs = arr_date.hour
    result= (arr_date-dep_date).total_seconds()//3600

    inp = [total_stops,dep_hrs,arr_hrs,result]+lst_2+lst+lst1

    pred = model.predict([inp])

    return render_template('index.html',prediction_text='The Predicted Flight Fare is Rs.{}'.format(round(pred[0])))




    
if __name__ == '__main__':
    app.run(debug=True)