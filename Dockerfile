# Poetry
FROM python:3.7 as requirements-stage
WORKDIR /tmp
RUN python -m pip install --upgrade pip
RUN python -m pip install poetry
COPY ./pyproject.toml ./poetry.lock* /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# Environement setup
FROM python:3.7-alpine as base
ARG UID=1000
ARG GID=1000
RUN addgroup -g "${GID}" python \
  && adduser -G python -u "${UID}" python -D
USER python
COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Production build
FROM base as runtime
WORKDIR /app
COPY --chown=python:python ./src/ /app/
CMD ["python", "-u", "run.py"]
