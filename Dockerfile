FROM python:3.14-slim

WORKDIR /app

ENV PYTHONPATH=/app

COPY ./requirements.txt /app/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY ./ /app/

CMD ["fastapi", "run", "src/backend/main.py", "--port", "80"]