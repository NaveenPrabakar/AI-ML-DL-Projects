# Use an official Python image as the base
FROM python:3.8-sli


WORKDIR /app


COPY model.py /app/


RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*


RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir transformers boto3

CMD ["python", "model.py"]
