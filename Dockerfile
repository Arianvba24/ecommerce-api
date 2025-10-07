FROM alpine:3.20

RUN apk add --no-cache \
    python3 py3-pip \
    build-base \
    libxml2-dev \
    libxslt-dev \
    python3-dev


COPY requirements.txt .

RUN pip install --no-cache-dir --break-system-packages -r requirements.txt


WORKDIR /fastapi_files

COPY . /fastapi_files

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
