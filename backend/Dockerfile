FROM python:3.10-slim-buster as prod

RUN pip install --upgrade pip && pip install poetry
WORKDIR /code
COPY poetry.lock pyproject.toml /code/
RUN poetry config virtualenvs.create false --local && \
    poetry install --no-root --no-interaction --no-ansi --without=dev
COPY . /code/
ENTRYPOINT ["/code/scripts/start.sh"]
EXPOSE 80

FROM prod as dev
RUN poetry install --no-root --no-interaction --no-ansi
