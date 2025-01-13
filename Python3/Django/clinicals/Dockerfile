FROM python:3.13

WORKDIR /djangoapps

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']

#docker build -f Dockerfile -t clinicals_app
#docker run -t --name=clinicals-app -p 8000:8000 clinicals_app
#docker exec -it clinicals-app bash
#docker exec -it clinicals-app python manage.py migrate