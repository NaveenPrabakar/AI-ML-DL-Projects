FROM public.ecr.aws/lambda/python:3.11

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy function code
COPY "Gemini.py" ${LAMBDA_TASK_ROOT}

# Set the handler (app.py → handler function)
CMD ["Gemini.handler"]
