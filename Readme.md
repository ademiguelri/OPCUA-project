# Communication via OPC UA
In this file ids explained how to run this project.

## Prerequisites
To run this project you need to have preinstalled some programs and python packages:
* Docker container
* OPCUA package for python
* Transitions package for python
* Threading package for python
* Psycopg2 package for python

## How to run
To run this program your first step is to run the docker compose file to start running the data recolection docker images.
>run this code in the parent folder, were the docke-compose.yml is located
```
docker compose up -d
```
Once all dockers are runnig, enter to the simulation folder and run the simulator.py file
```
python simulator.py
```
When the message of server listenning on ... appears, change to client_files folder and run the client.py file to start the client
```
python client.py
```
If the message "Client connected" the system will be exchanging data.

You can use OPC UA clients like UAExpert to change simulation target and power values.

## Run Grafana
When all the system is running in your favourite browser search for localhost:3000 to enter in grafana and watch the data that is reciveing the client. Also you can create your own dashboards to configure de data visualization to your liking.
