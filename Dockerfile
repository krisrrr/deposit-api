FROM python:3.11-alpine

COPY . .

RUN pip install -r requirements

EXPOSE 80/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
