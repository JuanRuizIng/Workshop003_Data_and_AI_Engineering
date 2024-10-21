FROM python:3.12-slim

WORKDIR /

COPY poetry.lock pyproject.toml .

RUN pip install poetry && poetry install

COPY . .

EXPOSE 5000

CMD ["python", "main.py"]