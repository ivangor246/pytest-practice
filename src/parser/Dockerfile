FROM python:3.13.2

WORKDIR /project

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENTRYPOINT [ "python", "app/main.py" ]
