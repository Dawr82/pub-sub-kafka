FROM python

RUN pip install pipenv

WORKDIR /producer

COPY ./Pipfile ./

RUN pipenv install

COPY ./src ./src

CMD ["pipenv", "run", "python", "src/producer.py"]

