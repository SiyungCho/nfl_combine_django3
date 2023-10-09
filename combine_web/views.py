from django.shortcuts import render, redirect, get_object_or_404
from .forms import input_data_Form
from .models import input_data
from django.contrib.auth.forms import UserCreationForm
import keras
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import OneHotEncoder, StandardScaler
import numpy as np
import os
from nfl_combine_web import settings

# Create your views here.
def home(request):
    return render(request, 'combine_web/home.html')

def input(request):
    if(request.method=='GET'):
        return render(request, 'combine_web/input.html', {'form':UserCreationForm()})
    else:
        mean_metrics={'mean_height':73.75, 'mean_weight':240.12, 'mean_40_yard':4.81, 'mean_bench_press':19.80, 'mean_vert_leap': 32.25, 'mean_broad_jump':113.28, 'mean_shuttle': 4.42, 'mean_3cone':7.31}
        try:
            form = input_data_Form(request.POST)
            new_player = form.save(commit=False)
            new_player.save()

            if float(new_player.player_Height) == 0.0:
                new_player.player_Height = mean_metrics['mean_height']

            if float(new_player.player_Weight) == 0.0:
                new_player.player_Weight = mean_metrics['mean_weight']

            if float(new_player.player_40Yard) == 0.0:
                new_player.player_40Yard = mean_metrics['mean_40_yard']

            if float(new_player.player_BenchPress) == 0.0:
                new_player.player_BenchPress = mean_metrics['mean_bench_press']

            if float(new_player.player_Vert) == 0.0:
                new_player.player_Vert = mean_metrics['mean_vert_leap']

            if float(new_player.player_Broad) == 0.0:
                new_player.player_Broad = mean_metrics['mean_broad_jump']

            if float(new_player.player_Shuttle) == 0.0:
                new_player.player_Shuttle = mean_metrics['mean_shuttle']

            if float(new_player.player_3Cone) == 0.0:
                new_player.player_3Cone = mean_metrics['mean_3cone']


            file_path = "combine_web/combine_prediction_model.keras"

            try:
                model = keras.models.load_model(file_path)
            except Exception as e:
                return render(request, 'combine_web/input.html', {'form':input_data_Form(), 'error':'Error occured in data passed'})
            
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
            
            prediction = model.predict(X_predict)

            new_player.prediction_score = round(prediction.item(),3)
            new_player.save()

            return redirect( 'output', object_id=new_player.pk)
        except ValueError:
            return render(request, 'combine_web/input.html', {'form':input_data_Form(), 'error':'Error occured in data passed'})
        
def output(request, object_id):
    player = get_object_or_404(input_data, pk=object_id)
    return render(request, 'combine_web/output.html', {'name':player.name,'score':player.prediction_score, 'object_id':object_id})

def prospects(request, object_id):

    if(object_id==0):
        df = pd.read_csv('combine_web/combine2023_preds.csv')
        combined_df = df.sort_values(by='Prediction Scores', ascending=False)
        combined_df['Prediction Scores'] = combined_df['Prediction Scores'].round(3)
        
        result_df = combined_df.head(5)
        result_worst_df = combined_df.tail(5)

        result_df.rename(columns={'Prediction Scores': 'Prediction_Scores'}, inplace=True)
        result_worst_df.rename(columns={'Prediction Scores': 'Prediction_Scores'}, inplace=True)

        return render(request, 'combine_web/prospects.html', {'top_player':result_df, 'top_POS_player': result_worst_df, 'object_id':object_id})
    else:
        player = get_object_or_404(input_data, pk=object_id)
        player_df = pd.DataFrame({'Name':[player.name], 'POS':[player.player_POS], 'Prediction Scores':[player.prediction_score]})
        df = pd.read_csv('combine_web/combine2023_preds.csv')
        combined_df = pd.concat([df, player_df], ignore_index=True)
        combined_df['Prediction Scores'] = combined_df['Prediction Scores'].round(3)

        combined_df = combined_df.sort_values(by='Prediction Scores', ascending=False)
        combined_df['Color'] = 'peachpuff'
        combined_df.loc[combined_df['Name'] == player.name, 'Color'] = 'salmon'

        position_data = combined_df[combined_df['POS'] == player.player_POS]
        
        plt.figure(figsize=(10, 6))
        plt.bar(position_data['Name'], position_data['Prediction Scores'], color=position_data['Color'])
        plt.xlabel('Player Name')
        plt.ylabel('Prediction Score')
        plt.title(f'Prediction Scores for {player.player_POS} Players')
        plt.xticks(rotation=45, ha='right')
            
        plt.tight_layout()

        media_dir = settings.MEDIA_ROOT
        graph_filename = 'my_graph.png'
        graph_path = os.path.join(media_dir, graph_filename)

        plt.savefig(graph_path, format='png')
        plt.close()

        if player.name not in combined_df['Name'][:5].values:
            player_data = {'Name': player.name, 'POS': player.player_POS, 'Prediction Scores': player.prediction_score}
            top_10_players = combined_df.head(4)
            result_df = pd.concat([top_10_players, pd.DataFrame([player_data])], ignore_index=True)
        else:
            result_df = combined_df.head(5)

        #top_player_POS = combined_df[combined_df['POS'] == player.player_POS].head(5)

        if player.name not in combined_df[combined_df['POS'] == player.player_POS][:5].values:
            top_player_POS = combined_df[combined_df['POS'] == player.player_POS].head(4)
            player_data = {'Name': player.name, 'POS': player.player_POS, 'Prediction Scores': player.prediction_score}
            result_POS_df = pd.concat([top_player_POS, pd.DataFrame([player_data])], ignore_index=True)
        else:
            top_player_POS = combined_df[combined_df['POS'] == player.player_POS].head(5)
            result_POS_df = top_player_POS

        result_df = result_df.drop(columns=["Color"])
        result_POS_df = result_POS_df.drop(columns=["Color"])

        result_df.rename(columns={'Prediction Scores': 'Prediction_Scores'}, inplace=True)
        result_POS_df.rename(columns={'Prediction Scores': 'Prediction_Scores'}, inplace=True)
        return render(request, 'combine_web/prospects.html', {'graph_url': os.path.join(settings.MEDIA_URL, graph_filename), 'top_player':result_df, 'top_POS_player': result_POS_df, 'object_id':object_id})