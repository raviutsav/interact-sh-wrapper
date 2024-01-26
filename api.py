from flask import Flask, request
import pandas as pd
import subprocess
import time
import re

app = Flask(__name__)

# Define a basic route

# this hash_map will store key as
# the url, value as the dataframe

# the dataframe structure will be
# column-> datetime | value |

central_data_repository = {}

def empty_file(file_path):
    open(file_path, 'w').close()

def read_and_store_data(file_path):
    with open(file_path, 'r') as file:
        for line in file:
            line = line.replace('\x00','')
            data_in_list = line.split(' ')
            print('LINEEE ' + line)
            link = data_in_list[0][1:-1]
            datestamp = data_in_list[-2]
            timestamp = data_in_list[-1]

            new_data = {'datetime': pd.to_datetime(datestamp + " " + timestamp), 'value': ' '.join(data_in_list[1:])}
            central_data_repository[link] = central_data_repository[link].append(new_data, ignore_index=True)
    
    empty_file(file_path)


@app.route('/')
def home():
    return 'Hello, World!\n'


@app.route('/getURL', methods=['GET'])
def getURL():
    empty_file('url.txt')
    read_and_store_data('output.txt')
    empty_file('output.txt')
    # start a new instance of interact.sh
    # command > out 2>error
    # ./program 2>&1 | tee a.txt
    # command = "./interactsh-client > output.txt 2>url.txt"
    # command = "./interactsh-client 2>&1 | tee url.txt"
    command = "(./interactsh-client | tee output.txt) 3>&1 1>&2 2>&3 | tee url.txt"

    file_path = 'url.txt'

    subprocess.Popen(command, shell=True, text=True)

    content = ''
    oast_link_regex = re.compile(r'.*oast.*')

    while len(content) == 0:
        with open(file_path, 'r') as file:
            content = file.read()
            content = oast_link_regex.findall(content)
    
    link = content[0].split()[1]
    print('my content is here ' + link)
    
    
    print("here is the link " + link)
    # Use re.search to check for a match

    df = pd.DataFrame(columns=['datetime', 'value'])
    central_data_repository[link.split('.')[0]] = df

    return link
    


@app.route('/getInteractions', methods=['GET'])
def getInteractions():
    read_and_store_data('output.txt')
    empty_file('output.txt')
    link = request.args.get('link').split('.')[0]

    isStartDateTimePresent = False
    isEndDateTimePresent = False

    if 'startDateTime' in request.args:
        isStartDateTimePresent = True
        start_datetime = request.args.get('startDateTime')
    if 'endDateTime' in request.args:
        isEndDateTimePresent = True
        end_datetime = request.args.get('endDateTime')
    
    if isStartDateTimePresent and isEndDateTimePresent:
        start_datetime = pd.to_datetime(start_datetime)
        end_datetime = pd.to_datetime(end_datetime)
    
    df = central_data_repository[link]
    def query_data(start_time, end_time):
        mask = (df['datetime'] >= start_time) & (df['datetime'] <= end_time)
        result = df[mask]
        return result
    

    if isStartDateTimePresent and isEndDateTimePresent:
        df = query_data(start_datetime, end_datetime)


    data_in_dict = df.to_dict()
    data_in_list = []

    for key, value in data_in_dict['value'].items():
        data_in_list.append(value)
    return data_in_list


if __name__ == '__main__':
    app.run(port=3000, debug=True)
