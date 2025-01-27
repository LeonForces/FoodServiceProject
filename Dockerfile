FROM python:3.12

RUN mkdir /food_app

WORKDIR /food_app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

RUN chmod a+x /food_app/docker/*.sh

CMD ["gunicorn src.main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000"]