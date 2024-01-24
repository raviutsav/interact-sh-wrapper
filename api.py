from flask import Flask
import subprocess

app = Flask(__name__)

# Define a basic route
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

    # Run the command and capture the output
    subprocess.Popen(command, shell=True, text=True)
    file_path = 'url.txt'  # Replace 'example.txt' with the path to your file

    with open(file_path, 'r') as file:
        content = file.read()
    
    return content
    


@app.route('/getInteractions', methods=['GET'])
def getInteractions():
    file_path = 'output.txt'  # Replace 'example.txt' with the path to your file

    
    with open(file_path, 'r') as file:
        content = file.read()
    
    return content


if __name__ == '__main__':
    app.run(port=3000, debug=True)
