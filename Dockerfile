FROM python:alpine3.19

ENV FLASK_APP=app.py

RUN mkdir -p /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir gunicorn

COPY src/ /app/

EXPOSE 8080

CMD ["gunicorn", "-w", "3", "-b", "0.0.0.0:8080", "--timeout", "120", "app:app"]
