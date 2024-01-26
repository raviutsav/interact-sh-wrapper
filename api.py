from flask import Flask, request, jsonify, make_response
import pandas as pd
import subprocess, re
from helper_functions import read_and_store_data, query_data, empty_file
app = Flask(__name__)

interaction_data = {}
urlFilePath = 'url.txt'
outputFilePath = 'output.txt'

@app.route('/')
def home():
    return 'Hello, World!\n'

@app.route('/getURL', methods=['GET'])
def getURL():

    try:
        empty_file(urlFilePath)
        read_and_store_data(outputFilePath, interaction_data)

        command = "(./interactsh-client | tee " + outputFilePath + ") 3>&1 1>&2 2>&3 | tee " + urlFilePath

        subprocess.Popen(command, shell=True, text=True)

        content = ''
        oast_link_regex = re.compile(r'.*oast.*')

        while len(content) == 0:
            with open(urlFilePath, 'r') as file:
                content = file.read()
                content = oast_link_regex.findall(content)
        
        link = content[0].split()[1]

        df = pd.DataFrame(columns=['datetime', 'value'])
        interaction_data[link.split('.')[0]] = df

        return link

    except Exception as e:
        print(f"An error occured: {e}")
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
        return response
    


@app.route('/getInteractions', methods=['GET'])
def getInteractions():

    try:
        read_and_store_data(outputFilePath, interaction_data)
        
        link = request.args.get('link').split('.')[0]

        if 'startDateTime' in request.args:
            start_datetime = pd.to_datetime(request.args.get('startDateTime'))
        else:
            start_datetime = pd.to_datetime('1970-01-01 00:00:00')

        if 'endDateTime' in request.args:
            end_datetime = pd.to_datetime(request.args.get('endDateTime'))
        else:
            end_datetime = pd.Timestamp.now()
        
        df = interaction_data[link]
        
        df = query_data(start_datetime, end_datetime, df)

        data_in_dict = df.to_dict()
        data_in_list = []

        for key, value in data_in_dict['value'].items():
            data_in_list.append(value)

        return data_in_list
    
    except Exception as e:
        print(f"An error occured: {e}")
        response = make_response(jsonify({'error': 'Internal Server Error'}), 500)
        return response


if __name__ == '__main__':
    app.run(port=3000, debug=True)
