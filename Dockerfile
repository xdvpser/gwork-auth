FROM python:3-alpine as build

WORKDIR /app/
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk add --no-cache postgresql-dev gcc musl-dev

COPY requirements/ requirements/
COPY requirements.txt .

RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt


FROM python:3-alpine

WORKDIR /app/
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY --from=build /app/wheels /wheels
COPY --from=build /app/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY . /app
RUN chmod +x scripts/entrypoint.sh
ENTRYPOINT [ "scripts/entrypoint.sh" ]
CMD [ "uvicorn", "app.auth:app", "--host", "0.0.0.0", "--reload" ]
