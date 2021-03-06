# django-rest-tutorial

## How to run
- Install project dependencies
```bash
$ pip3 install -r requirements.txt
```
- Run the frontend
```bash
$ python3 ./mysite/manage.py runserver 0.0.0.0:8000
```
- Run the eclipse mosquitto docker container
```bash
$ docker run -d -it -p 1883:1883 -v $(pwd)/mosquitto.conf:/mosquitto/config/mosquitto.conf eclipse-mosquitto
```
- Run the backend server
```bash
$ python3 ./gRPC_with_protobuf/server.py
```

## Using browser to perform client request
```
http://localhost:8000/rest/fibonacci 
http://localhost:8000/rest/logs

```
## All POST data type is JSON
## POST a order to calculate
in /rest/fibonacci
```
{"order":"<int>"}
```
## POST a command to clear histories
in /rest/fibonacci
```
{"clear":"<string>"}
```
the <string> is everything what you want to enter but "false".

[video link](https://drive.google.com/file/d/1l92_I2Am2UJ-7WoiIZP5XF_Cd19wFgx9/view?usp=sharing)