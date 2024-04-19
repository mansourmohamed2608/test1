# Yosr.ai
### Current UML
![Orders models](https://github.com/m-ayman-kh/yosr.ai/blob/main/myapp_models.png?raw=true)

to generate a new UML diagram 
```
python manage.py graph_models -a -o myapp_models.png   
```
### installation
1- clone the repo
```
git clone https://github.com/OmarSwailam/yosr.git
```
2- add virtualenv 
```
python -m venv venv
```
3- avtivate the virtualenv
```
./venv/scripts/activate
```
4- install the requirements
```
pip install -r requirements.txt
```
5- create a db named yosr

https://www.youtube.com/watch?v=2rqMRkVvXcw

6- migrate db migrations
```
python manage.py migrate
```
7-create an admin
```
python manage.py createsuperuser
```
8- start project
```
python manage.py runserver
```
now head to the http://localhost:8080/admin to interact with the models
