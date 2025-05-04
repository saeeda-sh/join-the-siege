FROM python:3.10-slim
WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libgl1-mesa-glx \
    tesseract-ocr \
    poppler-utils \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

ENV PYTHONUNBUFFERED=1 \
    FLASK_APP=src/app.py \
    FLASK_RUN_HOST=0.0.0.0

EXPOSE 5000

CMD ["python", "src/app.py"]
# CMD ["flask", "run"]