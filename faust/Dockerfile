FROM python:3.6.7

RUN pip3 install pipenv

COPY ./Pipfile ./Pipfile
RUN pipenv lock
RUN pipenv sync

# RUN pipenv shell

COPY ./requirements.txt  ./requirements.txt 
RUN pipenv install -r requirements.txt 

COPY . .

CMD ["pipenv","run", "python", "app.py"]