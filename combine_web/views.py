from django.shortcuts import render, redirect
from .forms import input_data_Form
from .models import input_data
from django.contrib.auth.forms import UserCreationForm
import tensorflow as tf
from tensorflow import keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import os

# Create your views here.
def home(request):
    return render(request, 'combine_web/base.html')

def input(request):
    if(request.method=='GET'):
        return render(request, 'combine_web/input.html', {'form':UserCreationForm()})
    else:
        try:
            form = input_data_Form(request.POST)
            new_player = form.save(commit=False)#don't put in database just yet
            new_player.save()

            file_path = "combine_web/combine_prediction_model.keras"

            try:
                model = tf.keras.models.load_model(file_path)
            except Exception as e:
                prediction = os.getcwd()
                model = None
            holder_df = pd.DataFrame(columns=['POS', "Height (in)", "Weight (lbs)", "40 Yard", "Bench Press", "Vert Leap (in)", "Broad Jump (in)", "Shuttle", "3Cone"])
            new_entry = pd.DataFrame({'POS': [new_player.player_POS], "Height (in)": [float(new_player.player_Height)], "Weight (lbs)": [float(new_player.player_Weight)], "40 Yard": [float(new_player.player_40Yard)], "Bench Press": [float(new_player.player_BenchPress)], "Vert Leap (in)": [float(new_player.player_Vert)], "Broad Jump (in)": [float(new_player.player_Broad)], "Shuttle": [float(new_player.player_Shuttle)], "3Cone": [float(new_player.player_3Cone)]})
            holder_df = pd.concat([holder_df,new_entry], ignore_index=True)
            sampled_df = pd.read_csv('combine_web/sampled_data.csv')
            sampled_df = sampled_df.drop(columns=["Pro Bowl"])
            pred_df = pd.concat([sampled_df, holder_df], ignore_index=True)
            categorical_col = ['POS']
            encoder = OneHotEncoder()
            encoded_features = encoder.fit_transform(pred_df[categorical_col]).toarray()
            numerical_col = ["Height (in)", "Weight (lbs)", "40 Yard", "Bench Press", "Vert Leap (in)", "Broad Jump (in)", "Shuttle", "3Cone"]
            scalar = StandardScaler()
            scaled_numerical_features = scalar.fit_transform(pred_df[numerical_col])
            pred_data = pd.concat([pd.DataFrame(encoded_features), pd.DataFrame(scaled_numerical_features)], axis=1)
            pred_input = pred_data.tail(1)
            X_predict = np.array(pred_input)
            if model is not None:
                prediction = model.predict(X_predict)

            return render(request, 'combine_web/output.html', {'name':prediction})
        except ValueError:
            return render(request, 'combine_web/input.html', {'form':input_data_Form(), 'error':'Error occured in data passed'})
        
def output(request):
    return render(request, 'combine_web/output.html')