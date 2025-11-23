FROM python:3.9-slim
WORKDIR /app
COPY Pipfile Pipfile.lock ./
RUN pip install pipenv && pipenv install --deploy
COPY . /app
ENV FLASK_APP=./src/main.py
ENV PYTHONPATH=/app
EXPOSE 5003
CMD ["pipenv", "run", "python", "src/main.py"]
