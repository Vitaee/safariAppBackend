FROM python:3.10

EXPOSE 8000
WORKDIR /source

COPY . /source

RUN pip install -U pip \
    && pip install poetry

RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi

CMD ["python","manage.py", "runserver", "--settings=safariBackend.settings.test", "0.0.0.0:8000"]