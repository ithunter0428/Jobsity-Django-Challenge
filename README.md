# Jobsity / Django-Challenge

## Description
https://git.jobsity.com/jobsity/django-challenge/-/tree/main
* Connected the two services via RabbitMQ
* Used Simple JWT instead of basic authentication
* Added unit tests

## Prerequisites
1. You are able to create a Django application and have basic understanding of how to build APIs using the [Django REST framework](https://www.django-rest-framework.org/).

2. Install [RabbitMQ](https://www.rabbitmq.com/) & Startup the local RabbitMQ Server.
* Install ErLang. You can get the latest Windows installer [here](https://www.erlang.org/download.html). Before we continue, ensure that the appropriate environment variable (`ERLANG_HOME`) has been created during the installation.

* Install RabbitMQ Service. Grab the latest installer for Windows from the RabbitMQ website [here](https://www.rabbitmq.com/install-windows.html).

* Navigate to the sbin directory of the RabbitMQ Server installation directory. In my case the path is
__C:\Program Files\RabbitMQ Server\rabbitmq_server-3.10.4\sbin__

* Run the following command to enable the plugin
```
  rabbitmq-plugins.bat enable rabbitmq_management
```

* Then, follow the commands below:
```
  rabbitmq-service.bat stop
  rabbitmq-service.bat install
  rabbitmq-service.bat start
```
To check if everything worked as expected, navigate to http://localhost:15672/mgmt. You will be prompted for username and password. The default credentials are:

username: `guest`

password: `guest`

3. You have installed `djangorestframework-simplejwt` & `pika` library. You can run the following:
```
  pip3 install djangorestframework-simplejwt
  pip3 install pika
```
4. A suitable IDE such as VS Code, Pycharm, etc.

## How to Run the Project
* Create a virtualenv:
```
  python -m venv virtualenv
  virtualenv/scripts/activate
```
* Install dependencies:
```
  pip install -r requirements.txt
```
* Start the Api_Service:
```
  cd api_service
  python manage.py makemigrations
  python manage.py migrate
  python manage.py createsuperuser
      username: admin
      email: admin@example.com
      password: 123456789
  python manage.py runserver
```
* Start the Stock_Service:
```
  cd stock_service
  python consumer.py
```
* Start the Front-End:
```
  cd frontend
  npm install
  npm run start:dev
```
You can login with __admin__ user.

## How to Test the Project
```
  cd api_service
  python manage.py test api
```
