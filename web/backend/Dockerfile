FROM python:3.6.7

RUN pip3 install pipenv
WORKDIR /app
ADD . /app
COPY ./Pipfile ./
RUN pipenv lock
RUN pipenv sync

COPY . .

# CMD ["pipenv","run", "python", "app.py"]
CMD ["pipenv", "run", "uwsgi", "app.ini" ]