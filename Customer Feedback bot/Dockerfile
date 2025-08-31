FROM public.ecr.aws/lambda/python:3.10

WORKDIR /app


COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt


COPY model.py ${LAMBDA_TASK_ROOT}
COPY SentimentModel/ ${LAMBDA_TASK_ROOT}/SentimentModel/

# Lambda handler entry point
CMD ["model.lambda_handler"]
