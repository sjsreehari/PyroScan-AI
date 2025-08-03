FROM python:3.11-slim

WORKDIR /

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

EXPOSE 8434

CMD ["python", "main.py"]
