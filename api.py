from flask import Flask
import subprocess
import re
import pandas as pd
import time

app = Flask(__name__)

# Define a basic route

hash_map = {}

@app.route('/')
def home():
    return 'Hello, World!\n'

@app.route('/getURL', methods=['GET'])
def getURL():
    # start a new instance of interact.sh
    # command > out 2>error
    # ./program 2>&1 | tee a.txt
    # command = "./interactsh-client > output.txt 2>url.txt"
    # command = "./interactsh-client 2>&1 | tee url.txt"
    command = "(./interactsh-client | tee output.txt) 3>&1 1>&2 2>&3 | tee url.txt"

    file_path = 'url.txt'

    # this will empty the file
    with open(file_path, 'w'):
        pass
    subprocess.Popen(command, shell=True, text=True)
    
    time.sleep(1)

    with open(file_path, 'r') as file:
        content = file.read()
    
    oast_link_regex = re.compile(r'.*oast.*')
    link = oast_link_regex.findall(content)[0].split()[1]
    print("here is the link " + link)
    # Use re.search to check for a match
    return link
    


@app.route('/getInteractions', methods=['GET'])
def getInteractions():
    file_path = 'output.txt'  # Replace 'example.txt' with the path to your file

    data = {
        'datatime': [],
        'value': []
    }
    with open(file_path, 'r') as file:
        for line in file:
            after_first_word_removed = line.split()[1:]
            datestamp = after_first_word_removed[-2]
            timestamp = after_first_word_removed[-1]

            row = ' '.join(after_first_word_removed)

            data['datatime'].append(datestamp + " " + timestamp)
            data['value'].append(row)
    
    df = pd.DataFrame(data)
    df['datatime'] = pd.to_datetime(df['datatime'])

    data_in_dict = df.to_dict()
    data_in_list = []

    for key, value in data_in_dict['value'].items():
        data_in_list.append(value)
    return data_in_list


if __name__ == '__main__':
    app.run(port=3000, debug=True)
