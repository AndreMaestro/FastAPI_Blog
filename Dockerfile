FROM python:3.13.13-alpine

ENV PATH="${PATH}:/root/.local/bin"
COPY ./src /app/src
COPY alembic /app/alembic
COPY alembic.ini /app/
COPY requirements.txt /app/
COPY ./image /app/image

ENV PYTHONPATH /app/src
WORKDIR /app
RUN pip install -r ./requirements.txt
RUN chmod +x ./src/start.sh
EXPOSE 8000