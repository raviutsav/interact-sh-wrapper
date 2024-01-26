from flask import Flask, request
import pandas as pd
import subprocess, re

app = Flask(__name__)

# central_data_repository will map 'link' to its corresponding dataframe
central_data_repository = {}
urlFilePath = 'url.txt'
outputFilePath = 'output.txt'

# function to clear the content of file
def empty_file(file_path):
    open(file_path, 'w').close()

# function to store the data in their corresponding dataframe
def read_and_store_data(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace('\x00','')
            data_in_list = line.split(' ')

            link = data_in_list[0][1:-1]
            datestamp = data_in_list[-2]
            timestamp = data_in_list[-1]

            new_data = {'datetime': pd.to_datetime(datestamp + " " + timestamp), 'value': ' '.join(data_in_list[1:])}
            central_data_repository[link] = central_data_repository[link].append(new_data, ignore_index=True)
    
    empty_file(file_path)

def query_data(start_time, end_time, df):
    mask = (df['datetime'] >= start_time) & (df['datetime'] <= end_time)
    result = df[mask]
    return result

@app.route('/')
def home():
    return 'Hello, World!\n'


@app.route('/getURL', methods=['GET'])
def getURL():
    empty_file(urlFilePath)
    read_and_store_data(outputFilePath)

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
    central_data_repository[link.split('.')[0]] = df

    return link
    


@app.route('/getInteractions', methods=['GET'])
def getInteractions():
    read_and_store_data(outputFilePath)
    
    link = request.args.get('link').split('.')[0]

    if 'startDateTime' in request.args:
        start_datetime = pd.to_datetime(request.args.get('startDateTime'))
    else:
        start_datetime = pd.to_datetime('1970-01-01 00:00:00')

    if 'endDateTime' in request.args:
        end_datetime = pd.to_datetime(request.args.get('endDateTime'))
    else:
        end_datetime = pd.Timestamp.now()
    
    df = central_data_repository[link]
    
    df = query_data(start_datetime, end_datetime, df)

    data_in_dict = df.to_dict()
    data_in_list = []

    for key, value in data_in_dict['value'].items():
        data_in_list.append(value)
        
    return data_in_list


if __name__ == '__main__':
    app.run(port=3000, debug=True)
