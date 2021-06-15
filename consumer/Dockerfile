FROM python

RUN pip install pipenv

WORKDIR /consumer

COPY ./Pipfile ./

RUN pipenv install

COPY ./src ./src

CMD ["pipenv", "run", "python", "src/consumer.py"]