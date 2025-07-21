FROM python:3.13.2

WORKDIR /project

COPY requirements.txt .

RUN pip install --upgrade pip --no-cache-dir \
    && pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONPATH="/project"

ENTRYPOINT [ "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload" ]
