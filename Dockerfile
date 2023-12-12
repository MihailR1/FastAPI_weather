FROM python:3.11-alpine

WORKDIR /new_app

RUN python -m pip install --upgrade pip

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--port=80"]
