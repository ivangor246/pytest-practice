FROM python:3.13.2

RUN apt-get update \
    && apt-get install -y netcat-traditional

WORKDIR /project

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT [ "python", "main.py" ]
