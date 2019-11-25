FROM python:3.6.7

RUN pip3 install pipenv

COPY ./Pipfile ./Pipfile
RUN pipenv lock
RUN pipenv sync

COPY . .

CMD ["pipenv","run", "python", "app.py"]