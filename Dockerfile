FROM python:3.10

WORKDIR /app

COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN apt-get update && apt-get install -y nodejs npm
RUN cd resumelens-ui && npm install && npm run build

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]