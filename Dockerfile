FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

EXPOSE 8080

RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
