Video for demo purpose can be viewed from: https://youtu.be/hclpewyrDqM
Docker hub link of the image: https://hub.docker.com/repository/docker/raviutsav/interactsh-wrapper/general
To run this program locally

without Docker
--------------
make sure -> you are on unix distro(required for running interacrsh-client)
          -> have installed python 3.7+

install pandas and flask using 
```
pip install pandas flask
```
To run the program, open the project folder and run following commnad
```
python3 api.py
```

with Docker
-----------
run following command in the project folder
```
docker build -t <docker-image-name> .
```
upon successful completion of above command run
```
docker run -p 3000:3000 <docker-image-name>
```


This wrapper is collection of 2 APIs.

1) /getURL
2) /getInteraction


/getURL
This endpoint returns a runs an instance of interactsh-client and returns the URL corresponding to it.
```
http://127.0.0.1:3000/getURL
```

/getInteraction
This endpoint returns the interactions made by users on the url provided by the interactsh-client.

This api takes three query parameter
1) link -> this is the url for which you want to see interactions (needed)
2) startDateTime -> specifying this query parameter will filter the interactions to show only those interactions which happend after <startDateTime>. Default is 1970-01-01 00:00:00 
3) endDateTime -> specifying this query paramter will filer the interactions to show only those interactions which happened before <endDateTime> Defailt is current time

usage examples
```
http://127.0.0.1:3000/getInteraction?link=ghdwsbgfoiawebgoihagirbg.oast.mov
http://127.0.0.1:3000/getInteraction?link=ghdwsbgfoiawebgoihagirbg.oast.mov&startDateTime=1970-01-01%2000:00:00 
http://127.0.0.1:3000/getInteraction?link=ghdwsbgfoiawebgoihagirbg.oast.mov&endDateTime=2024-01-01%2000:00:00
http://127.0.0.1:3000/getInteraction?link=ghdwsbgfoiawebgoihagirbg.oast.mov&startDateTime=1970-01-01%2000:00:00&endDateTime=2024-01-01%2000:00:00
```
