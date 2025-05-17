FROM python:3.11-slim-buster
#FROM python:3.11-slim

#ENV PYTHONDONTWRITEBYTECODE=1
#ENV PYTHONUNBUFFERED=1

#WORKDIR /app
WORKDIR /backend-docker

#COPY . /app/

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY . .

#EXPOSE 5004

CMD ["python", "main.py"]
#CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
