# Safari Mobile App Backend
A backend rest api project which follows best practices of SDLC. Developing for a mobile application.  

### Some Features:
- Compliance with the principles of test writing DRF
- Compliance with the principles of clean coding
- Dockerized
- Using the nginx web server
- Documented and visualized by Swagger

### Run project with docker
I assume that you installed docker & docker compose on your OS. Clone the project from github then, in terminal which opened in project root directory:

- type ```docker compose build```
- type ```docker compose up -d```
- Elastic search integrated to the project so after above commands connect each web service e.g:
- ```docker exec -it safariappbakcend-web-1 bash``` then type:
- type ```python manage.py search_index --rebuild --settings=safariBackend.settings.test```
- Now we are free to go, visit ```http://127.0.0.1:70/swagger``` to watch the api documentation.
- for development run ```python manage.py runserver --settings=safariBackend.settings.test```.