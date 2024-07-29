FROM python:3.9.19-slim-bullseye

WORKDIR /app

COPY requirements.txt /app

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 3000

CMD [ "python", "run.py" ]
