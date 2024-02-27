FROM python:3.11-alpine

COPY . .

RUN pip install -r requirements

EXPOSE 8000

CMD ["uvicorn", "main:app"]
