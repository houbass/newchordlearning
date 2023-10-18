#WEB API LIB
from flask import Flask
from flask import request
from flask_cors import CORS
import json
import time

#MACHINE LEARNING LIB
import pandas as pd
#machine learning algorythm (decisin tree)
from sklearn.tree import DecisionTreeClassifier

#CREATING FLASK APP
app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

#MACHINE LEARNING
#IMPORT DATA
music_data_major = pd.read_csv("chords.csv")
music_data_minor = pd.read_csv("chords_minor.csv")


#API
@app.route('/', methods = ["GET", "POST"])
def handle_request():
    
    input = str(request.args.get("input"))  #request the input

    music_index = int(input[0])
    music_data_all = [music_data_major, music_data_minor]
    music_data = music_data_all[music_index]

    searching_inputs = [["1ch", "1v"], ["1ch", "1v", "2ch", "2v"], ["1ch", "1v", "2ch", "2v", "3ch", "3v"] ]
    searching_outputs = [["2ch", "2v"], ["3ch", "3v"], ["4ch", "4v"]]

    data = []
    
    if input == "None":
        input = "makato"
    
    else:
        #FINDING SECOND CHORD
        first_chord = input[1] + input[2]        
        
        #prepare data to right format
        res1 = [eval(i) for i in first_chord]

        #input dataset
        X1 = music_data[searching_inputs[0]]

        #output dataset
        y1 = music_data[searching_outputs[0]]

        #adding datasets to model (input, output)
        model1 = DecisionTreeClassifier()
        model1.fit(X1,y1)

        #making prediction of next chord (position / voicing)
        prediction1 = model1.predict([ res1 ])
        value11 = str(prediction1[0][0])
        value21 = str(prediction1[0][1])
        this_prediction1 = value11 + value21
            
            
        #FINDING THIRD CHORD     
        second_input = first_chord + this_prediction1

        #prepare data to right format
        res2 = [eval(i) for i in second_input]
        
        #input dataset
        X2 = music_data[searching_inputs[1]]    
        
        #output dataset
        y2 = music_data[searching_outputs[1]]    
        
        #adding datasets to model (input, output)
        model2 = DecisionTreeClassifier()
        model2.fit(X2,y2)
        
        #making prediction of next chord (position / voicing)
        prediction2 = model2.predict([ res2 ])
        value12 = str(prediction2[0][0])
        value22 = str(prediction2[0][1])
        this_prediction2 = value12 + value22      
        
        
        #FINDING FOURTH CHORD     
        third_input = first_chord + this_prediction1 + this_prediction2

        #prepare data to right format
        res3 = [eval(i) for i in third_input]

        #input dataset
        X3 = music_data[searching_inputs[2]]     
        
        #output dataset
        y3 = music_data[searching_outputs[2]] 
        
        #adding datasets to model (input, output)
        model3 = DecisionTreeClassifier()
        model3.fit(X3,y3)
        
        #making prediction of next chord (position / voicing)
        prediction3 = model3.predict([ res3 ])
        value13 = str(prediction3[0][0])
        value23 = str(prediction3[0][1])
        this_prediction3 = value13 + value23        
        
        
        chords = [first_chord, this_prediction1, this_prediction2, this_prediction3]    
        data = chords


    data_set = {"input": input, "prediction": data}
    json_dump = json.dumps(data_set)

    return json_dump