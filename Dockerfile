FROM python:3.10

WORKDIR /app

ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PIP_ROOT_USER_ACTION=ignore
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt update
RUN apt install -y --no-install-recommends

COPY pyproject.toml /app/

COPY . /app

RUN pip install poetry \
    && pip install django-crispy-forms \
    && poetry config installer.max-workers 10 \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi -vvv

RUN python manage.py makemigrations
RUN python manage.py migrate

EXPOSE 8000